from flask import Blueprint, render_template, request, jsonify, current_app
import pandas as pd
import folium, os
import requests


mapapi_bp = Blueprint('mapapi_bp', __name__)

menu = {'ho':0, 'ol':0, 'ba':0, 'fr':0, 'mp':1 }

def get_dataframe():
    filename = os.path.join(current_app.static_folder, 'data', '서울부동산.csv')
    return pd.read_csv(filename)

def map_by_dong(df, dong):
    gf = df[df.BJDONG_NM.str.contains(dong, na=False)]
    m = folium.Map([gf.위도.mean(), gf.경도.mean()], zoom_start=15)
    for i in gf.index:
        tooltip = f"{gf.CMP_NM[i]}<br>{gf.ADDRESS[i]}<br>{gf.RA_REGNO[i]}"
        popup_html = f"""
            <div class="popup-content-wrapper" style="white-space: nowrap;">
                <div class="popup-content" style="cursor: pointer;" onclick="showDetails('{gf.CMP_NM[i]}', '{gf.ADDRESS[i]}', '{gf.RA_REGNO[i]}')">
                    {gf.CMP_NM[i]}<br>{gf.ADDRESS[i]}<br>{gf.RA_REGNO[i]}
                </div>
            </div>
        """
        folium.Marker([gf.위도[i], gf.경도[i]], tooltip=tooltip, popup=folium.Popup(html=popup_html, parse_html=False)).add_to(m)
    return m._repr_html_()

@mapapi_bp.route('/mapapi', methods=['GET', 'POST'])
def mapapi():
    if request.method == 'GET':
        return render_template('mapapi/mapapi.html', menu=menu)
    else:
        df = get_dataframe()
        dong = request.form.get('dong')
        map_html = map_by_dong(df, dong)
        return jsonify({'map_html': map_html})

@mapapi_bp.route('/get_map/<dong>')
def get_map(dong):
    df = get_dataframe()
    map_html = map_by_dong(df, dong)
    return jsonify({'map_html': map_html})
