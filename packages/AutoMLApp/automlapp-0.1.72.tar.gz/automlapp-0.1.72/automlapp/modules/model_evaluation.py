from utils.streamlit_utils import st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import confusion_matrix, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, auc, roc_curve
from sklearn.metrics import ConfusionMatrixDisplay

class ModelEvaluation:
	def __init__(_self, df, X_train, y_train, X_test, y_test):
		_self.df = df
		_self.X_train = X_train
		_self.y_train = y_train
		_self.X_test = X_test
		_self.y_test = y_test
		_self.plot_colors = px.colors.sequential.Blues[::-2]

	def evaluate_models(_self):
		if 'trained_models' in st.session_state and len(st.session_state.trained_models) != 0 and st.session_state.eval:
			target = st.session_state.target
			st.subheader("Evaluation Metrics")
			
			eval_df, eval_df_formatted = pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]), pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])
			if _self.df[target].nunique() > 2:
				avg = 'micro'
			else:
				avg = 'binary'
			for model, name in zip(st.session_state.trained_models, st.session_state.model_names):
				y_pred = model.predict(_self.X_test)
				prob = model.predict_proba(_self.X_test)[:, 1]
				fpr, tpr, thresholds = roc_curve(_self.y_test, prob)

				row_df = pd.DataFrame({
					"Model": [name],
					"Accuracy": [accuracy_score(_self.y_test, y_pred)],
					"Precision": [precision_score(_self.y_test, y_pred, average=avg)],
					"Recall": [recall_score(_self.y_test, y_pred, average=avg)],
					"F1 Score": [f1_score(_self.y_test, y_pred, average=avg)],
					"AUC": [auc(fpr, tpr)],
					"Gini": [2 * auc(fpr, tpr) - 1],
					"KS": [np.max(tpr - fpr)]
				})
				row_df_formatted = pd.DataFrame({
					"Model": [name],
					"Accuracy": [f"{accuracy_score(_self.y_test, y_pred):.2%}"],
					"Precision": [f"{precision_score(_self.y_test, y_pred, average=avg):.2%}"],
					"Recall": [f"{recall_score(_self.y_test, y_pred, average=avg):.2%}"],
					"F1 Score": [f"{f1_score(_self.y_test, y_pred, average=avg):.2%}"],
					"AUC": [f"{auc(fpr, tpr):.2%}"],
					"Gini": [f"{2 * auc(fpr, tpr) - 1:.2%}"],
					"KS": [f"{np.max(tpr - fpr):.2%}"]
				})
				eval_df = pd.concat([eval_df, row_df], ignore_index=True)
				eval_df_formatted = pd.concat([eval_df_formatted, row_df_formatted], ignore_index=True)
				st.session_state.eval_df = eval_df
			# st.table(eval_df_formatted)
			st.dataframe(eval_df_formatted, use_container_width=True)

			fig = px.bar(
				eval_df.set_index("Model"), 
				orientation='h', 
				width=980,
				color_discrete_sequence=_self.plot_colors
			)
			fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), yaxis={'categoryorder':'total ascending'})
			st.write(fig)

			st.subheader("Confusion Matrix")
			cols = st.columns(len(st.session_state.trained_models))
			for i, col in enumerate(cols):
				col.write(st.session_state.model_names[i])
				y_pred = st.session_state.trained_models[i].predict(_self.X_test)
				
				# Compute the confusion matrix
				cm = confusion_matrix(_self.y_test, y_pred)
				
				# Normalize the confusion matrix by row (i.e by the number of samples in each class)
				cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
				
				# Create a new DataFrame for the confusion matrix
				cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
				
				# Format the DataFrame to include percentages
				for j in range(cm_df.shape[0]):
					for k in range(cm_df.shape[1]):
						cm_df.iloc[j, k] = f"{cm[j, k]} ({cm_normalized[j, k]*100:.1f}%)"
				
				# Display the confusion matrix
				col.table(cm_df)

	def evaluate_custom_models(_self):
		if 'trained_models_custom' in st.session_state and len(st.session_state.trained_models_custom) != 0:
			target = st.session_state.target
			st.subheader("Evaluation Metrics of Model Trained on Custom Hyperparameters")
			
			eval_df_custom, eval_df_custom_formatted = pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]), pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])
			if _self.df[target].nunique() > 2:
				avg = 'micro'
			else:
				avg = 'binary'
			for model, name in zip(st.session_state.trained_models_custom, st.session_state.custom_model_names):
				y_pred = model.predict(_self.X_test)
				prob = model.predict_proba(_self.X_test)[:, 1]
				fpr, tpr, thresholds = roc_curve(_self.y_test, prob)

				row_df = pd.DataFrame({
					"Model": [name],
					"Accuracy": [accuracy_score(_self.y_test, y_pred)],
					"Precision": [precision_score(_self.y_test, y_pred, average=avg)],
					"Recall": [recall_score(_self.y_test, y_pred, average=avg)],
					"F1 Score": [f1_score(_self.y_test, y_pred, average=avg)],
					"AUC": [auc(fpr, tpr)],
					"Gini": [2 * auc(fpr, tpr) - 1],
					"KS": [np.max(tpr - fpr)]
				})
				row_df_formatted = pd.DataFrame({
					"Model": [name],
					"Accuracy": [f"{accuracy_score(_self.y_test, y_pred):.2%}"],
					"Precision": [f"{precision_score(_self.y_test, y_pred, average=avg):.2%}"],
					"Recall": [f"{recall_score(_self.y_test, y_pred, average=avg):.2%}"],
					"F1 Score": [f"{f1_score(_self.y_test, y_pred, average=avg):.2%}"],
					"AUC": [f"{auc(fpr, tpr):.2%}"],
					"Gini": [f"{2 * auc(fpr, tpr) - 1:.2%}"],
					"KS": [f"{np.max(tpr - fpr):.2%}"]
				})
				eval_df_custom = pd.concat([eval_df_custom, row_df], ignore_index=True)
				eval_df_custom_formatted = pd.concat([eval_df_custom_formatted, row_df_formatted], ignore_index=True)
				st.session_state.eval_df_custom = eval_df_custom
			# st.table(eval_df_custom_formatted)
			st.dataframe(eval_df_custom_formatted, use_container_width=True)

			fig = px.bar(
				eval_df_custom.set_index("Model"), 
				orientation='h', 
				width=980,
				color_discrete_sequence=_self.plot_colors
			)
			fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), yaxis={'categoryorder':'total ascending'})
			st.write(fig)

			st.subheader("Confusion Matrix")
			cols = st.columns(len(st.session_state.trained_models_custom))
			for i, col in enumerate(cols):
				col.write(st.session_state.custom_model_names[i])
				y_pred = st.session_state.trained_models_custom[i].predict(_self.X_test)
				
				# Compute the confusion matrix
				cm = confusion_matrix(_self.y_test, y_pred)
				
				# Normalize the confusion matrix by row (i.e by the number of samples in each class)
				cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
				
				# Create a new DataFrame for the confusion matrix
				cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
				
				# Format the DataFrame to include percentages
				for j in range(cm_df.shape[0]):
					for k in range(cm_df.shape[1]):
						cm_df.iloc[j, k] = f"{cm[j, k]} ({cm_normalized[j, k]*100:.1f}%)"
				
				# Display the confusion matrix
				col.table(cm_df)

	def evaluate_tuned_models(_self):
		if 'tuned_models' in st.session_state and len(st.session_state.tuned_models) != 0:
			target = st.session_state.target
			st.subheader("Evaluation Metrics after tuning the hyperparameters")
			
			eval_df_tuned, eval_df_tuned_formatted = pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]), pd.DataFrame(columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"])
			if _self.df[target].nunique() > 2:
				avg = 'micro'
			else:
				avg = 'binary'
			for model, name in zip(st.session_state.tuned_models, st.session_state.tuned_model_names):
				y_pred = model.predict(_self.X_test)
				prob = model.predict_proba(_self.X_test)[:, 1]
				fpr, tpr, thresholds = roc_curve(_self.y_test, prob)

				# Get the previous scores for the current model
				prev_scores = st.session_state.eval_df[st.session_state.eval_df['Model'] == name].iloc[0]

				# Calculate the metrics first
				accuracy = accuracy_score(_self.y_test, y_pred)
				precision = precision_score(_self.y_test, y_pred, average=avg)
				recall = recall_score(_self.y_test, y_pred, average=avg)
				f1 = f1_score(_self.y_test, y_pred, average=avg)
				auc_score = auc(fpr, tpr)
				gini = 2 * auc_score - 1
				ks = np.max(tpr - fpr)

				# Calculate the deltas
				delta_accuracy = accuracy - float(prev_scores['Accuracy'])
				delta_precision = precision - float(prev_scores['Precision'])
				delta_recall = recall - float(prev_scores['Recall'])
				delta_f1 = f1 - float(prev_scores['F1 Score'])
				delta_auc = float(auc_score - prev_scores['AUC'])
				delta_gini = gini - float(prev_scores['Gini'])
				delta_ks = ks - float(prev_scores['KS'])

				# Create a grid of columns
				cols = st.columns(7)

				# Display the metrics with deltas in the grid
				st.subheader(name)
				cols[0].metric(label = "Accuracy", value = f"{accuracy:.2%}", delta = f"{delta_accuracy:.2%}")
				cols[1].metric(label = "Precision", value = f"{precision:.2%}", delta = f"{delta_precision:.2%}")
				cols[2].metric(label = "Recall", value = f"{recall:.2%}", delta = f"{delta_recall:.2%}")
				cols[3].metric(label = "F1 Score", value = f"{f1:.2%}", delta = f"{delta_f1:.2%}")
				cols[4].metric(label = "AUC", value = f"{auc_score:.2%}", delta = f"{delta_auc:.2%}")
				cols[5].metric(label = "Gini", value = f"{gini:.2%}", delta = f"{delta_gini:.2%}")
				cols[6].metric(label = "KS", value = f"{ks:.2%}", delta = f"{delta_ks:.2%}")

				row_df = pd.DataFrame({
					"Model": [name],
					"Accuracy": [accuracy],
					"Precision": [precision],
					"Recall": [recall],
					"F1 Score": [f1],
					"AUC": [auc_score],
					"Gini": [gini],
					"KS": [ks]
				})
				row_df_formatted = pd.DataFrame({
					"Model": [name],
					"Accuracy": [f"{accuracy_score(_self.y_test, y_pred):.2%}"],
					"Precision": [f"{precision_score(_self.y_test, y_pred, average=avg):.2%}"],
					"Recall": [f"{recall_score(_self.y_test, y_pred, average=avg):.2%}"],
					"F1 Score": [f"{f1_score(_self.y_test, y_pred, average=avg):.2%}"],
					"AUC": [f"{auc(fpr, tpr):.2%}"],
					"Gini": [f"{2 * auc(fpr, tpr) - 1:.2%}"],
					"KS": [f"{np.max(tpr - fpr):.2%}"]
				})
				eval_df_tuned = pd.concat([eval_df_tuned, row_df], ignore_index=True)
				eval_df_tuned_formatted = pd.concat([eval_df_tuned_formatted, row_df_formatted], ignore_index=True)
			# st.table(eval_df_tuned_formatted)
			st.dataframe(eval_df_tuned_formatted, use_container_width=True)
			st.session_state.eval_df_tuned = eval_df_tuned_formatted

			fig = px.bar(
				eval_df_tuned.set_index("Model"), 
				orientation='h', 
				width=980,
				color_discrete_sequence=_self.plot_colors
			)
			fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), yaxis={'categoryorder':'total ascending'})
			st.write(fig)

			st.subheader("Confusion Matrix")
			cols = st.columns(len(st.session_state.tuned_models))

			for i, col in enumerate(cols):
				col.write(st.session_state.tuned_model_names[i])
				y_pred = st.session_state.tuned_models[i].predict(_self.X_test)
				
				# Compute the confusion matrix
				cm = confusion_matrix(_self.y_test, y_pred)
				
				# Normalize the confusion matrix by row (i.e by the number of samples in each class)
				cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
				
				# Create a new DataFrame for the confusion matrix
				cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
				
				# Format the DataFrame to include percentages
				for j in range(cm_df.shape[0]):
					for k in range(cm_df.shape[1]):
						cm_df.iloc[j, k] = f"{cm[j, k]} ({cm_normalized[j, k]*100:.1f}%)"
				
				# Display the confusion matrix
				col.table(cm_df)
	
	def calculate_deciles(_self, model_type, model_name, subset):
		if model_type == "Model With Default Hyperparameters":
			model = st.session_state.trained_models_dict[str(model_name)]
		elif model_type == "Model With Tuned Hyperparameters":
			model = st.session_state.tuned_models_dict[str(model_name)]
		elif model_type == "Model With Custom Hyperparameters":
			model = st.session_state.trained_models_custom_dict[str(model_name)]
			
		if subset == "train":
			df_copy = pd.concat([_self.X_train, _self.y_train], axis = 1)
			df_copy['default'] = model.predict(_self.X_train)
			df_copy['prob'] = model.predict_proba(_self.X_train)[:, 1]
		elif subset == "test":
			df_copy = pd.concat([_self.X_test, _self.y_test], axis = 1)
			df_copy['default'] = model.predict(_self.X_test)
			df_copy['prob'] = model.predict_proba(_self.X_test)[:, 1]

		df_copy = df_copy.sort_values(by = 'prob', ascending = False)

		df_copy['decile'] = pd.qcut(df_copy['prob'], 10, labels = False)

		# Add 1 to make deciles 1 to 10
		df_copy['decile'] = df_copy['decile'] + 1

		output = df_copy.groupby('decile').agg(
			decile_score = ('decile', 'min'),
			population_count = ('decile', 'size'),
			bad_count = ('Bad_gt500_final', 'sum')
		)

		# Calculate good count
		output['good_count'] = output['population_count'] - output['bad_count']

		# Calculate response rate
		output['bad_rate'] = round((output['bad_count'] / output['population_count']) * 100, 2)

		# percentage of defaults in each decile
		total_bad = output['bad_count'].sum()
		output['bad_percentage'] = round((output['bad_count'] / total_bad) * 100, 2)

		# percentage good in each decile
		total_good = output['good_count'].sum()
		output['good_percentage'] = round((output['good_count'] / total_good) * 100, 2)

		# Sort by decile
		output.sort_values(by = 'decile', inplace = True, ascending = False)
		output.reset_index(drop = True, inplace = True)

		# Calculate cumulative good and bad count
		output['cumulative_good_count'] = output['good_count'].cumsum()
		output['cumulative_bad_count'] = output['bad_count'].cumsum()

		# Calculate cumulative good and bad percentage
		output['cumulative_bad_perc'] = output['bad_percentage'].cumsum()
		output['cumulative_good_perc'] = output['good_percentage'].cumsum()

		# Calculate cumulative sample size and cumulative default rate
		output['cumulative_population_count'] = output['population_count'].cumsum()

		# Calculate KS statistic
		output['KS'] = output['cumulative_bad_perc'] - output['cumulative_good_perc']

		result = output.loc[:,['decile_score', 'population_count', 'cumulative_population_count', 'good_count', 'bad_count', 'bad_rate', 'cumulative_good_count', 'cumulative_bad_count', 'cumulative_good_perc', 'cumulative_bad_perc', 'KS']]
		st.dataframe(result)