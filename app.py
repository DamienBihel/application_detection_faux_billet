from flask import Flask, render_template, request, make_response, url_for, send_file
import pickle
import pandas as pd
import io
import os

app = Flask(__name__)

# Charger le modèle de régression logistique
with open('model_LogisticRegression.sav', 'rb') as f:
    model = pickle.load(f)


# Route principale
@app.route('/')
def hello_world():
    return render_template('index.html')


# Route pour la prédiction et l'affichage des résultats
@app.route('/result', methods=['POST'])
def predict():
    file = request.files['file']
    df = pd.read_csv(file, sep=',')
    data_clean = df.dropna()

    # Prédiction avec le modèle
    y_pred = model.predict(data_clean.select_dtypes(exclude='object'))
    proba_pred = model.predict_proba(data_clean.select_dtypes(exclude='object'))

    # Ajout des résultats de la prédiction au dataframe
    data_result = data_clean.copy()
    data_result['résultat'] = y_pred
    code = {1: 'Vrai billet', 0: 'Faux billet'}
    data_result['résultat'] = data_result['résultat'].map(code)

    # Calcul du nombre de billets vrais et faux
    nb_vrais_billets = data_result[data_result['résultat'] == 'Vrai billet']
    nb_faux_billets = data_result[data_result['résultat'] == 'Faux billet']

    # affichage des probabilités
    data_result['proba_pred_faux'] = proba_pred[:, 0]
    data_result['proba_pred_vrai'] = proba_pred[:, 1]

    # Enregistrement du fichier CSV dans le dossier static
    static_folder = os.path.join(app.root_path, 'static')
    csv_file = os.path.join(static_folder, 'result.csv')
    data_result.to_csv(csv_file, index=False)

    # Création de la réponse pour le téléchargement
    response = make_response(data_result.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    response.headers["Content-Type"] = "text/csv"

    # Ajout d'un lien de téléchargement pour le fichier CSV
    download_link = f"<a href='{url_for('download', filename='result.csv')}' class='result'>Télécharger les " \
                    f"résultats</a>"

    # Affichage des résultats
    data_result_no_dim = data_result.drop(
        ['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length'], axis=1)

    return render_template('result.html', download_link=download_link, data=data_result_no_dim.to_html(),
                           nb_vrais_billets=len(nb_vrais_billets), nb_faux_billets=len(nb_faux_billets))


# Route pour le téléchargement du fichier CSV des résultats
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.root_path, 'static', filename)
    if os.path.exists(path):
        with open(path, 'rb') as fileresult:
            output = io.BytesIO(fileresult.read())
        return send_file(output, as_attachment=True, download_name=filename, mimetype='text/csv')
    else:
        return "Le fichier n'existe pas."


if __name__ == '__main__':
    app.run()
