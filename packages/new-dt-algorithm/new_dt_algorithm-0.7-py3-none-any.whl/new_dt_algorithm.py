class new_dt_algorithm:
    def __init__(self):
        """
        Initialize the object with default attributes.
        """
        self.model = None
        self.test_data = None
        self.train_data = None
        self.mi_features = None
        self.ks_features = None
        self.original_filtered_vars = None
        self.anova_features = None
        self.iv_features = None
        self.logit_features = None
        self.non_ml_features = None
        self.rf_features = None
        self.final_features = None

    def read_data(self, data, Target, na_impute=-99999):
        """
        Read data and preprocess it.

        Parameters:
            data (DataFrame): Input DataFrame.
            Target (str): Name of the target variable.
            na_impute (int, optional): Value to use for imputing missing values. Default is -99999.
        """
        import pandas as pd
        self.__init__()
        self.data = data
        self.Target = Target.lower()
        self.data.columns = self.data.columns.str.lower()
        self.data[self.Target] = pd.to_numeric(self.data[self.Target], errors='coerce')
        self.data = self.data.dropna(axis=1, how="all")
        self.data = self.data.dropna(axis=0, how="all")
        self.data = self.data.fillna(na_impute)
        
        for col in self.data.columns:
            if self.data[col].nunique() <= 1:
                del self.data[col]
            else:    
                try:
                    pd.to_numeric(self.data[col])
                except Exception as e: 
                    if (self.data[col].nunique() > 25) or (len(self.data[col].astype(str).str.split('-').loc[0]) > 1):
                        del self.data[col]
                    else:
                        self.data = pd.get_dummies(self.data, columns=[col])
        
        for col in self.data.columns:
            self.data[col] = pd.to_numeric(self.data[col])
            if self.data[col].value_counts().reset_index().shape[0] == 2:
                self.data[col] = self.data[col].astype(int)      
        
        self.data = self.data.drop([x for x in list(self.data.columns) if 'unnamed' in x], axis=1)

    def iv_woe(self, data, target, bins=10, show_woe=False):
        """
        Calculate Information Value (IV) and Weight of Evidence (WoE) for given data and target variable.

        Parameters:
            data (DataFrame): Input DataFrame containing independent variables and the target variable.
            target (str): Name of the target variable.
            bins (int): Number of bins for continuous variables.
            show_woe (bool): Flag to display the WoE table.

        Returns:
            DataFrame: DataFrame containing IV values for each independent variable.
            DataFrame: DataFrame containing WoE values for each category of each independent variable.
        """
        import pandas as pd
        import numpy as np

        newDF, woeDF = pd.DataFrame(), pd.DataFrame()

        # Extract column names of independent variables
        selected_features = list(data.drop([target], axis=1).columns)

        # Calculate WoE and IV for each independent variable
        for ivar in selected_features:
            if (data[ivar].dtype.kind in 'bifc') and (len(np.unique(data[ivar])) > 10):
                # For continuous variables, discretize into bins
                binned_x = pd.qcut(data[ivar], bins, duplicates='drop')
                d0 = pd.DataFrame({'x': binned_x, 'y': data[target]})
            else:
                d0 = pd.DataFrame({'x': data[ivar], 'y': data[target]})

            # Calculate counts and sums for events and non-events
            d = d0.groupby("x", as_index=False).agg({"y": ["count", "sum"]})
            d.columns = ['Cutoff', 'N', 'Events']
            d['% of Events'] = np.maximum(d['Events'], 0.5) / d['Events'].sum()
            d['Non-Events'] = d['N'] - d['Events']
            d['% of Non-Events'] = np.maximum(d['Non-Events'], 0.5) / d['Non-Events'].sum()
            d['WoE'] = np.log(d['% of Events'] / d['% of Non-Events'])
            d['IV'] = d['WoE'] * (d['% of Events'] - d['% of Non-Events'])
            d.insert(loc=0, column='Variable', value=ivar)

            # Concatenate IV values
            temp = pd.DataFrame({"Variable": [ivar], "IV": [d['IV'].sum()]}, columns=["Variable", "IV"])
            newDF = pd.concat([newDF, temp], axis=0)

            # Concatenate WoE values
            woeDF = pd.concat([woeDF, d], axis=0)

            # Show WoE table
            if show_woe:
                print(d)

        return newDF, woeDF





    def filtering_features(self, test_cutoff=0.10, iv_cutoff=0.005, ml_cutoff=100000, rf_cutoff=0.80):
        """
        Filter features using multiple iterations of feature selection methods.

        Parameters:
            test_cutoff (float, optional): Test cutoff value. Default is 0.10.
            iv_cutoff (float, optional): Information value (IV) cutoff value. Default is 0.005.
            ml_cutoff (int, optional): Multicollinearity cutoff value. Default is 100000.
            rf_cutoff (float, optional): Random forest cutoff value. Default is 0.80.

        Returns:
            None
        """
        import numpy as np
        import  warnings
        warnings.filterwarnings('ignore')
        import pandas as pd
        from sklearn.feature_selection import mutual_info_classif
        from scipy.stats import kruskal, f_oneway
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
        from sklearn.ensemble import RandomForestClassifier
        import statsmodels.api as sm
        
        self.test_cutoff = test_cutoff
        self.iv_cutoff = iv_cutoff
        self.ml_cutoff = ml_cutoff
        self.rf_cutoff = rf_cutoff
        # First iteration based on mutual information
        if self.final_features is None:
            if self.mi_features is None:
                mi_values = mutual_info_classif(self.data, self.data[[self.Target]])
                top_k_indices = np.argsort(mi_values)[::-1][:]
                top_k_features = self.data.columns[top_k_indices]
                mi_features = [feature for feature, mi_val in zip(top_k_features, mi_values[top_k_indices]) if mi_val > 0]

                print(f"{len(mi_features)} features remaining out of {self.data.shape[1]} after mutual information test iteration")
                self.mi_features = mi_features

            # Second iteration based on statistical test 
            if self.ks_features is None:
                ks_features = []
                for feature in self.mi_features:
                    result = kruskal(*[self.data[self.mi_features][self.data[self.mi_features][self.Target] == group][feature] for group in self.data[self.mi_features][self.Target].unique()])
                    if result.pvalue < self.test_cutoff:
                        ks_features.append(feature)

                print(f"{len(ks_features)} features remaining out of {len(self.mi_features)} after Kruskal test iteration")    
                self.ks_features = ks_features  

            if self.anova_features is None:
                anova_features = []
                for feature_column in self.ks_features:  
                    groups = [self.data[self.ks_features][self.data[self.ks_features][self.Target] == cls][feature_column] for cls in self.data[self.ks_features][self.Target].unique()]
                    f_statistic, p_value = f_oneway(*groups)
                    if p_value < self.test_cutoff:
                        anova_features.append(feature_column)

                print(f"{len(anova_features)} features remaining out of {len(self.ks_features)} after ANOVA test iteration")             
                self.anova_features = anova_features 

            # Fourth iteration based on information value
            if self.iv_features is None:
                iv, woe = self.iv_woe(data=self.data[self.anova_features], target=self.Target, bins=10, show_woe=False)
                iv_features = iv[iv['IV'] > self.iv_cutoff]['Variable'].to_list()        

                print(f"{len(iv_features)} features remaining out of {len(self.anova_features)} after IV test iteration")  
                self.iv_features = iv_features       

            # Fifth and sixth iterations based on refinement using L1 regularization and removing multicollinearity
            if self.logit_features is None:      
                X_train, X_test, y_train, y_test = train_test_split(self.data[self.iv_features], self.data[[self.Target]], test_size=0.2, random_state=42)
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                log_reg = LogisticRegression(penalty='l1', solver='liblinear', random_state=42)
                log_reg.fit(X_train_scaled, y_train)
                selected_features_indices = np.where(log_reg.coef_ != 0)[1]
                logit_features = list(X_train[X_train.columns[selected_features_indices]].columns)

                print(f"{len(logit_features)} features remaining out of {len(self.iv_features)} after L1 Logistic iteration")  
                self.logit_features = logit_features    

            if self.non_ml_features is None:
                scaler = StandardScaler()
                X_scaled_ml = scaler.fit_transform(self.data[self.logit_features])
                X_scaled_ml = pd.DataFrame(X_scaled_ml, columns=self.logit_features)
                vif_data = pd.DataFrame()
                vif_data["Variable"] = ['var']
                vif_data["VIF"] = [1000000000000]
                def compute_vif(col):
                    temp = pd.DataFrame({'Variable': col, 'VIF': 1 / (1 - sm.OLS(X_scaled_ml[col].values, sm.add_constant(X_scaled_ml.drop(col, axis=1))).fit().rsquared_adj)}, index=[0])                            
                    return temp
                while vif_data["VIF"].max() > self.ml_cutoff: 
                    vif_data = pd.concat([compute_vif(col) for col in list(X_scaled_ml.columns)], axis=0).reset_index(drop=True)
                    max_vif_variable = vif_data[vif_data['VIF'] == vif_data['VIF'].max()]['Variable'].to_list()[0]
                    if vif_data["VIF"].max() > self.ml_cutoff:
                        X_scaled_ml = X_scaled_ml.drop(columns=max_vif_variable)
                non_ml_features = list(X_scaled_ml.columns) 

                print(f"{len(non_ml_features)} features remaining out of {len(self.logit_features)} after multicollinearity iteration") 
                self.non_ml_features = non_ml_features

            # Seventh iteration based on Random Forest 
            if self.rf_features is None:
                X_train, X_test, y_train, y_test = train_test_split(self.data[self.non_ml_features], self.data[[self.Target]], test_size=0.2, random_state=42)
                model = RandomForestClassifier(n_estimators=int(len(self.non_ml_features)/4),
                                               min_samples_leaf=int((self.data.shape[0]/int(len(self.non_ml_features)/4))*0.05),
                                               max_samples=0.5, max_depth=3)
                model.fit(X_train, y_train)
                feature_importance_df = pd.DataFrame({
                    'Feature': X_train.columns ,
                    'Importance': model.feature_importances_
                })
                feature_importance_df = feature_importance_df.sort_values(['Importance'], ascending=False)
                for i in feature_importance_df['Importance']:
                    if feature_importance_df[feature_importance_df['Importance'] >= i]['Importance'].sum() >= self.rf_cutoff:
                        final_imp_vars = feature_importance_df[feature_importance_df['Importance'] >= i]['Feature'].to_list()
                        break        

                print(f"{len(final_imp_vars)} features remaining out of {len(self.non_ml_features)} after Random Forest iteration")        
                self.rf_features = final_imp_vars

                self.final_features = final_imp_vars
                self.original_filtered_vars = final_imp_vars

                
    def add_or_remove_feature(self, addition_feature_name=None, removing_feature_name=None):
        """
        Add or remove a feature from the dataset.

        Parameters:
            addition_feature_name (str): The name of the feature to add.
            removing_feature_name (str): The name of the feature to remove.

        Returns:
            None
        """
        # Ensure that features have been filtered first
        if self.final_features is None:
            print('Please filter features first.')
        else:
            # Add a feature if addition_feature_name is provided and it exists in the dataset
            if addition_feature_name is not None:
                if addition_feature_name in self.data.columns:
                    self.final_features.append(addition_feature_name)

            # Remove a feature if removing_feature_name is provided and it exists in the final features
            if removing_feature_name is not None:
                if removing_feature_name in self.final_features:
                    self.final_features.remove(removing_feature_name)
                              
        


    def training_decision_tree(self, min_pop_per=0.05, max_pop_per=0.20, max_depth=3, test_size=0.2):
        """
        Train a decision tree model with specified parameters.

        Parameters:
            min_pop_per (float): Minimum population percentage for leaf nodes.
            max_pop_per (float): Maximum population percentage for leaf nodes.
            max_depth (int): Maximum depth of the decision tree.
            test_size (float): Size of the test dataset.

        Returns:
            None
        """
        # Save the current feature combination
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        import pandas as pd
        current_combination = self.final_features

        # Initialize lists to store random state and bad difference values
        random_st = []
        bad_diff_value = []

        # Iterate over random states
        for i in range(1, 100):
            # Split data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(self.data[current_combination], 
                                                                self.data[[self.Target]], 
                                                                test_size=test_size, 
                                                                random_state=i, 
                                                                stratify=self.data[self.Target])

            # Create copies of the datasets
            original_dataset_train = pd.concat([pd.DataFrame(X_train, columns=X_train.columns),
                                                pd.DataFrame(y_train, columns=[self.Target])], axis=1)
            original_dataset_test = pd.concat([pd.DataFrame(X_test, columns=X_test.columns),
                                               pd.DataFrame(y_test, columns=[self.Target])], axis=1)

            # Create copies for manipulation
            X_t_test = original_dataset_test.copy()
            subset_data = original_dataset_train.copy()

            # Prepare data for model training
            X_t = subset_data.drop([self.Target], axis=1)
            y_t = subset_data[self.Target]

            # Train the decision tree model
            model = DecisionTreeClassifier(random_state=42, max_depth=max_depth,
                                           min_samples_leaf=int(round((subset_data.shape[0]) * min_pop_per, 0)))
            model.fit(X_t, y_t)

            # Calculate predicted probabilities
            X_t_test['predict_prob'] = model.predict_proba(X_t_test.drop([self.Target], axis=1))[:, 1]
            X_t_test['dummy'] = 1

            # Calculate population percentage and bad rate
            def custom_sum_product(group):
                return pd.Series({'Pop%': group['dummy'].sum() / X_t_test.shape[0],
                                  'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

            X_t_test = X_t_test.groupby('predict_prob').apply(custom_sum_product).reset_index()

            # Calculate bad difference value
            if (X_t_test.reset_index()['Pop%'].max()<=max_pop_per)&(X_t_test.reset_index()['Pop%'].min()>=min_pop_per):
                bad_diff = abs((X_t_test['predict_prob'] - X_t_test['bad_rate']) * X_t_test['Pop%']).sum()
                bad_diff_value.append(bad_diff)
            else:
                bad_diff_value.append(100)
            random_st.append(i)

        # Find the random state with the lowest bad difference value
        results = pd.DataFrame({'random_state': random_st, 'bad_diff': bad_diff_value})
        results = results[results['bad_diff'] == results['bad_diff'].min()]

        # Handle multiple best results
        if results.shape[0] > 1:
            ran_state = 42
            print('Please adjust min_max_pop split.')
        else:
            ran_state = results.reset_index()['random_state'].tolist()[0]

        # Train the decision tree model with the selected random state
        X_train, X_test, y_train, y_test = train_test_split(self.data[current_combination], 
                                                            self.data[[self.Target]], 
                                                            test_size=test_size, 
                                                            random_state=ran_state, 
                                                            stratify=self.data[self.Target])

        # Create copies of the datasets
        original_dataset_train = pd.concat([pd.DataFrame(X_train, columns=X_train.columns),
                                            pd.DataFrame(y_train, columns=[self.Target])], axis=1)
        original_dataset_test = pd.concat([pd.DataFrame(X_test, columns=X_test.columns),
                                           pd.DataFrame(y_test, columns=[self.Target])], axis=1)

        # Prepare data for model training
        X_t_test = original_dataset_test.copy()
        subset_data = original_dataset_train.copy()

        X_t = subset_data.drop([self.Target], axis=1)
        y_t = subset_data[self.Target]

        # Update train and test datasets and save the trained model
        self.test_data = X_t_test.copy()
        self.train_data = subset_data.copy()
        model = DecisionTreeClassifier(random_state=42, max_depth=max_depth,
                                       min_samples_leaf=int(round((subset_data.shape[0]) * min_pop_per, 0)))
        model.fit(X_t, y_t)
        self.model = model




    def plot_current_tree(self, figure_size=(30, 25), fontsize=10):
        """
        Plot the current decision tree model.

        Parameters:
            figure_size (tuple): Size of the figure.
            fontsize (int): Font size of the plot.

        Returns:
            None
        """
        # Check if the model has been trained
        if self.model is None:
            print('Please train the model first.')
        else:
            # Plot the decision tree
            import matplotlib.pyplot as plt
            from sklearn.tree import plot_tree
            plt.figure(figsize=figure_size)
            plot_tree(self.model, 
                      feature_names=self.final_features, 
                      class_names=[str(c) for c in self.data[self.Target].unique()], 
                      filled=True, 
                      fontsize=fontsize, 
                      rounded=True, 
                      proportion=True)
            plt.show()
            
    def performance_current_tree(self):
        """
        Evaluate the performance of the current tree model using training and test data.

        Prints the population percentage and bad rate for different predicted probabilities.

        Returns:
            None
        """
        # Check if the model has been trained
        if self.model is None:
            print('Please train the model first.')
        else:
            # Performance evaluation on training data
            import pandas as pd
            import matplotlib.pyplot as plt
            from sklearn.tree import plot_tree
            train_data = self.train_data.copy()
            train_data['predict_prob'] = self.model.predict_proba(train_data.drop([self.Target], axis=1))[:, 1]
            train_data['dummy'] = 1

            def custom_sum_product(group):
                return pd.Series({'Pop%': group['dummy'].sum() / train_data.shape[0],
                                  'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

            train_result = train_data.groupby('predict_prob').apply(custom_sum_product)
            print("Training Data:")
            print(train_result)

            # Performance evaluation on test data
            test_data = self.test_data.copy()
            test_data['predict_prob'] = self.model.predict_proba(test_data.drop([self.Target], axis=1))[:, 1]
            test_data['dummy'] = 1

            def custom_sum_product(group):
                return pd.Series({'Pop%': group['dummy'].sum() / test_data.shape[0],
                                  'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

            test_result = test_data.groupby('predict_prob').apply(custom_sum_product)
            print("\nTest Data:")
            print(test_result)
