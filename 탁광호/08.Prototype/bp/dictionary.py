from flask import Blueprint, render_template, current_app, request



dictionary_bp = Blueprint('dictionary_bp', __name__)

menu = {'ho':0, 'ol':0, 'ba':1, 'fr':0, 'mp':0 }

@dictionary_bp.route('/jeonse')
def jeonse():
    print(current_app.root_path)       #bp module에서는 app 대신에 current_app을 사용
    return render_template('/dictionary/jeonse.html',  menu=menu)

@dictionary_bp.route('/wolse')
def wolse():
    print(current_app.root_path)
    return render_template('/dictionary/wolse.html',  menu=menu)


@dictionary_bp.route('/tip')
def tip():    
    print(current_app.root_path)
    return render_template('/dictionary/tip.html',  menu=menu)



