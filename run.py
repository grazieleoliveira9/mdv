from app import app

if __name__ == '__main__':
    app.run(debug=True)




from app import app

print("Rotas registradas:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)