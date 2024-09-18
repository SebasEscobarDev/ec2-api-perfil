from flask import Flask, request, jsonify

app = Flask(__name__)

def validar_datos(birth_info):
    # Validar que todos los campos requeridos estén presentes
    required_fields = ['nombre', 'año', 'mes', 'dia']
    for field in required_fields:
        if field not in birth_info or birth_info[field] is None:
            return False

    # Validar que los valores sean razonables
    try:
        año = int(birth_info['año'])
        mes = int(birth_info['mes'])
        dia = int(birth_info['dia'])

        if not (1900 <= año <= 2100):
            return False
        if not (1 <= mes <= 12):
            return False
        if not (1 <= dia <= 31):
            return False

    except ValueError:
        return False

    return True

@app.route('/perfil', methods=['POST'])
def natal_report():
    birth_info = None

    # Manejar diferentes tipos de contenido
    if request.content_type.startswith('application/json'):
        birth_info = request.json
    elif request.content_type.startswith('multipart/form-data'):
        birth_info = {
            'nombre': request.form.get('persona[nombre]'),
            'año': request.form.get('persona[año]'),
            'mes': request.form.get('persona[mes]'),
            'dia': request.form.get('persona[dia]')
        }
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

    # Validar los datos recibidos
    if not birth_info or not validar_datos(birth_info):
        return jsonify({"error": "Datos inválidos"}), 400

    # Texto fijo a devolver si los datos son válidos
    report_dict = [
        'Esta persona se caracteriza por ser emprendedora y tener un temperamento impulsivo y apasionado. Posee un espíritu aventurero, gran iniciativa y creatividad, y no se preocupa demasiado por el pasado o el presente. Tiene confianza en sí misma y tiene un alma de líder; está constantemente buscando nuevos caminos para alcanzar sus metas. Sin embargo, su ansiedad puede impedirle ser perseverante y lo hace sentir agobiado por la monotonía. A veces carece de diplomacia y olvida considerar a los demás, lo que puede exponer su egoísmo. La enorme ambición lo motiva a destacarse y mostrar sus habilidades, y siempre busca la acción e innovación para lograr los mejores resultados.',
        'Es una persona con una gran capacidad de percepción y perspicacia. Su carácter es firme y decidido, y sus sentimientos son profundos e intensos. Siente una gran atracción por los misterios y tiende a expresar abiertamente lo que piensa y siente, lo cual a veces puede lastimar a los demás. Aunque es poco demostrativo en cuanto a mostrar sus emociones, esto se debe en parte a su temor a ser vulnerable y perder el control. Como resultado, suele reprimir sus sentimientos.',
        'Es una persona es cariñosa, madura y extremadamente emotiva, y su estado de ánimo es variable. Es romántica y posee una gran ternura, emocionándose cuando se siente amada y comprendida. Además, es susceptible, soñadora y espiritual, comprensiva y generosa, entregándose de forma incondicional a quienes ama. Esta persona también posee facultades intuitivas e imaginativas, y generalmente tiene razón en sus suposiciones. Es bondadosa, alegre y divertida, con una gran habilidad para resolver misterios y trabajar de forma silenciosa y rápida. Le agrada la poesía, la música y los momentos de soledad, que le ayudan a reflexionar y planificar el futuro. Le gusta dejarse guiar por su imaginación, idealismo y presentimiento, siguiendo siempre sus sentimientos y lo que le sugiere su corazón.',
        'Es una persona que suele idealizar a su pareja y que busca la armonía y la paz en la relación amorosa. Puede ser un tanto inseguro en sus relaciones, buscando constantemente la aprobación y el cariño de su pareja. A veces puede caer en el victimismo y en la dependencia emocional, lo que puede llevar a situaciones de desequilibrio en la relación. Sin embargo, su profundo amor y entrega pueden hacer que sea una pareja muy valorada y querida por aquellos que lo rodean.',
        'Esta persona se caracteriza por su independencia y claridad de ideas, así como por su vida hiperactiva y constante iniciativa, lo que conlleva muchos cambios. Es impulsivo, impaciente y siempre piensa en el futuro, anhelando un porvenir despejado. Su espíritu emprendedor, audaz y aventurero le lleva a poner en práctica rápidamente cualquier idea que se le ocurra. Además, posee una capacidad innata de liderazgo y expresa sus deseos con intensidad. Aunque a veces puede actuar de forma impulsiva y sin reflexionar lo suficiente, su entusiasmo y arrebato son contagiosos, lo que lo convierte en una persona atractiva y carismática. No obstante, puede tener dificultades para perseverar en sus proyectos y a veces abandona uno para perseguir algo más interesante. Aspira a hacer las cosas a su manera y a liderar a otros hacia el éxito.',
        'Este individuo es un ser social y comunicativo que disfruta de mantener largas conversaciones y conocer bien a las personas que lo rodean. Es tolerante y comprensivo para evitar conflictos innecesarios, y utiliza la razón, el sentido común y la paciencia para lograr sus metas. Tiene la necesidad de transmitir las experiencias vividas, examinar y comprender lógicamente su entorno. Es una persona simpática, alegre, sociable y hospitalaria que se gana fácilmente el cariño de los demás. No le gusta la soledad y valora mucho la importancia de estar en pareja. Además, posee talento artístico y es una persona abierta y nada egoísta, capaz de tratar a todo el mundo con imparcialidad y cortesía. Siempre busca crecer y mejorar, manteniendo una actitud equilibrada y objetiva en todo momento.',
        'Esta persona logra todo lo que se propone con razón, sentido común y paciencia. Siente la necesidad de transmitir las experiencias vividas, examinar y comprender su entorno de manera lógica. Es muy estimado/a por aquellos que lo/la conocen, y se caracteriza por ser serio/a, honrado/a y estar en busca siempre de paz y armonía. Las relaciones ocupan un lugar importante en su vida, y es fiel tanto con sus amistades como con su cónyuge. Su matrimonio será beneficioso y los lazos que los unen estarán bien consolidados. Esta persona no evita el esfuerzo necesario para conservar una relación sana, y su manera de enaltecer sus promesas y deberes puede brindarle un sentimiento de intensa satisfacción.',
        'Es un individuo impetuoso y apasionado, altamente susceptible e intuitivo, que se enfoca completamente en lograr sus objetivos. A menudo es temido por su habilidad para detectar los puntos débiles de los demás y saber cuándo y cómo utilizarlos. Sin embargo, también puede ser un tanto negativo y depresivo cuando las cosas no salen según lo planeado. No tolera la traición y por lo general compite por mantener el control de las situaciones. Es ardiente, apasionado y tierno, aunque su inseguridad emocional lo perturba profundamente, lo que lo lleva a experimentar celos con frecuencia. Este individuo está dispuesto a arriesgarlo todo por las personas que ama y cuenta con una gran cantidad de energía que a veces se manifiesta de manera inesperada. Ama intensamente la vida y trabaja incansablemente para preservar la ecología. En una relación, es alguien que entrega todo de sí mismo y espera lo mismo o incluso más de su pareja.'
    ]

    # Devolver el texto fijo como JSON si los datos son válidos
    return jsonify(report_dict)

if __name__ == '__main__':
    app.run(port=5001)