from flask import Blueprint, render_template, current_app, request



fraud_bp = Blueprint('fraud_bp', __name__)

menu = {'ho':0, 'ol':0, 'ba':0, 'fr':1, 'mp':0 }

@fraud_bp.route('/camouflagedProperty')
def camouflagedProperty():
    print(current_app.root_path)       #bp module에서는 app 대신에 current_app을 사용
    return render_template('/fraud/camouflagedProperty.html',  menu=menu)

@fraud_bp.route('/priceManipulation')
def priceManipulation():
    print(current_app.root_path)
    return render_template('/fraud/priceManipulation.html',  menu=menu)


@fraud_bp.route('/JeonseFraud')
def JeonseFraud():    
    print(current_app.root_path)
    return render_template('/fraud/JeonseFraud.html',  menu=menu)

@fraud_bp.route('/RentalContract')
def RentalContract():    
    print(current_app.root_path)
    return render_template('/fraud/RentalContract.html',  menu=menu)

@fraud_bp.route('/RealEstateInvestment')
def RealEstateInvestment():    
    print(current_app.root_path)
    return render_template('/fraud/RealEstateInvestment.html',  menu=menu)



