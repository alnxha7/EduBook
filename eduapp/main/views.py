from django.shortcuts import render

def home(request):
    courses = [
        {'title': 'Python', 'description': 'Learn Python like a Professional Start from the basics and go all the way to creating your own applications and games'},
        {'title': 'Data Science', 'description': 'Learn how to use NumPy, Pandas, Seaborn , Matplotlib , Plotly , Scikit-Learn , Machine Learning, Tensorflow , and more!'},
        {'title': 'MERN Stack Web Development', 'description': 'Fullstack web development MERN STACK, ChatGPT, Node/Express, React, Mongodb, Javascript, HTML/CSS, build 9+ projects'},
        {'title': 'Flutter', 'description': 'A Complete Guide to the Flutter SDK &amp; Flutter Framework for building native iOS and Android apps'}
    ]
    contact_info = {
        'email1': 'milumathew7779@gmail.com',
        'email2': 'alansha71011@gmail.com',
        'offices': ['EduApp 2nd floor Technoark phase I: Trivandrum, Kerala', 
                    'EduApp 4th floor Infoark phase III: Ernakulam, Kerala', 
                    'EduApp 10th floor Prince Info City II: Chennai, Tamil Nadu']
    }
    context = {
        'courses': courses,
        'contact_info': contact_info
    }
    return render(request, 'main/home.html', context)
