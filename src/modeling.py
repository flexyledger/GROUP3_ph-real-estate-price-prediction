import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_model(model, X_test, y_test, is_log_target=True):
    """
    Evaluates a model and returns RMSE, MAE, and R2.
    If the target was log-transformed, it reverses the transformation 
    to calculate metrics on the original scale (PHP).
    """
    y_pred = model.predict(X_test)
    
    if is_log_target:
        y_test_orig = np.expm1(y_test)
        y_pred_orig = np.expm1(y_pred)
    else:
        y_test_orig = y_test
        y_pred_orig = y_pred
        
    rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred_orig))
    mae = mean_absolute_error(y_test_orig, y_pred_orig)
    r2 = r2_score(y_test_orig, y_pred_orig)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2
    }

def cross_validate_model(model, X, y, cv=5, is_log_target=True):
    """
    Performs cross validation and returns average metrics.
    """
    scoring = ['neg_root_mean_squared_error', 'neg_mean_absolute_error', 'r2']
    
    cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring, return_train_score=False)
    
    # Note: These metrics are on the log scale if the target is log scale
    return {
        'CV_RMSE_mean': -cv_results['test_neg_root_mean_squared_error'].mean(),
        'CV_RMSE_std': cv_results['test_neg_root_mean_squared_error'].std(),
        'CV_MAE_mean': -cv_results['test_neg_mean_absolute_error'].mean(),
        'CV_R2_mean': cv_results['test_r2'].mean()
    }

def compare_models(models_dict, X_train, y_train, cv=5):
    """
    Compares multiple models using cross-validation.
    """
    results = []
    
    for name, model in models_dict.items():
        cv_res = cross_validate_model(model, X_train, y_train, cv=cv)
        cv_res['Model'] = name
        results.append(cv_res)
        
    df_results = pd.DataFrame(results)
    # Reorder columns
    cols = ['Model', 'CV_RMSE_mean', 'CV_RMSE_std', 'CV_MAE_mean', 'CV_R2_mean']
    return df_results[cols].sort_values('CV_RMSE_mean')

def tune_hyperparameters(model, param_grid, X_train, y_train, cv=5):
    """
    Performs GridSearchCV to find best hyperparameters.
    """
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring='neg_root_mean_squared_error',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV RMSE (log scale): {-grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_
