print(user_df.shape)
y_pred = sc_model.predict(user_df)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)