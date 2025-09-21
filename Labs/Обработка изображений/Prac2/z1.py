def createDict():
    doctor = dict.fromkeys(['speciality', 'expirience', 'pacients'])
    # print(doctor)
    doctor['name'] = 'Petr'
    doctor['surname'] = 'Ivanov'
    doctor['patronymic'] = 'Mikhaolovich'
    print(doctor,end="\n\n")

    doctor['speciality'] = 'Surgeon'
    doctor['expirience'] = '25y'
    doctor['pacients'] = 'Ivanov', 'Petrov', 'Sidorov'

    print(dict.keys(doctor),end="\n\n")

    print(dict.items(doctor),end="\n\n")

    del doctor['patronymic']
    print(dict.keys(doctor),end="\n\n")

    print(doctor['surname'])

    print(doctor['speciality'],end="\n\n")

def make_doctor_01(surname, name, expirience): 
    return {'Surname': surname, 'Name': name, 'Expirience': expirience}

def make_doctor_02(surname, name, expirience, patients):
    return {'Surname': surname, 'Name': name, 'Expirience': expirience, 'Patients': patients}

listDoctor = [make_doctor_01('Ivanov', 'Ivan', 5), make_doctor_01('Petrov', 'Petr', 7), make_doctor_01('Sidorov', 'Sidor', 9)]

def make_patient_01(surname, name, city):
    return {'Surname': surname, 'Name': name, 'City': city}

def add_years_old_patient(patient, year):
    patient['year'] = year

def add_years_old_doctor(doctor, year):
    doctor['year'] = year

def add_phone_patient(patient, phone):
    patient['phone'] = phone

def add_gender_patient(patient, gender):
    patient['gender'] = gender

def add_gender_doctor(doctor, gender):
    doctor['gender'] = gender

if __name__ == '__main__':
    print("task 1\n")
    createDict()

    print("task 2\n")
    print(make_doctor_01('Ivanov', 'Ivan', 5),end="\n\n")

    print("task 3\n")
    print(make_doctor_02('Petrov', 'Petr', 7, 'Stalin'),end="\n\n")

    print("task 4\n")
    listDoctor = [make_doctor_01('Sidorov', 'Sidr', 3), make_doctor_01('Andreev', 'Andrey', 6), make_doctor_01('Miheev', 'Mihail', 9)]
    print(listDoctor, end="\n\n")

    print("task 5\n")
    print(make_patient_01('Stalin', 'Iosif', 'Moscow'),end="\n\n")

    print("task 6\n")
    patient1 = make_patient_01('Stalin', 'Iosif', 'Moscow')
    patient2 = make_patient_01('Lenin', 'Vladimir', 'Moscow')
    add_years_old_patient(patient1, 1950)
    add_years_old_patient(patient2, 1920)
    print(patient1)
    print(patient2, end="\n\n")

    print("task 7\n")
    doctor1 = make_doctor_01('Kudr', 'Alex', 30)
    doctor2 = make_doctor_02('Fillin', 'Fill', 40, {'Lenin'})
    add_years_old_doctor(doctor1, 1970)
    add_years_old_patient(doctor2, 1980)
    print(doctor1)
    print(doctor2, end="\n\n")

    print("task 8\n")
    list = [doctor1, doctor2]
    for i in range(len(list)):
        print('Возраст', i+1, 'врача:', (2022-list[i].get('year')), 'лет', end="\n\n")

    print("task 9\n")
    list = [patient1, patient2]
    for i in range(len(list)):
        print('Возраст', i+1, 'пациента:', (2022-list[i].get('year')), 'лет', end="\n\n")
    
    print("task 10\n")
    listPatients = [make_patient_01('Denisov', 'Denis', 'Samara'), make_patient_01('Voronov', 'Maxim', 'Sochi'),
                    make_patient_01('Ganin', 'Semen', 'Tolyatti')]
    for i in range(len(listPatients)):
        print('Фамилия:', listPatients[i].get('Surname'), 'Город:', listPatients[i].get('City'), end="\n\n")
    
    print("task 11\n")
    for i in listPatients[0].keys():
        print(i)

    print("task 12\n")
    for i in listDoctor[0].keys():
        print(i)
    
    print("task 13\n")
    plenty = dict(make_doctor_01('Kudr', 'Alex', 30))
    plenty.update(make_doctor_02('Fillin', 'Fill', 40, {'Lenin'}))
    print(plenty.keys(), end="\n\n")

    print("task 14\n")
    for i in listPatients[0].values():
        print(i)
    print(end="\n\n")

    print("task 15\n")
    for i in listDoctor[0].values():
        print(i)
    print(end="\n\n")

    print("task 16\n")
    patient1 = make_patient_01('Kudr', 'Alex', 30)
    patient2 = make_patient_01('Fillin', 'Fill', 25)
    add_phone_patient(patient1, 880005553535)
    add_phone_patient(patient2, 755544433227)
    print(patient1)
    print(patient2, end="\n\n")

    print("task 17\n")
    add_gender_patient(patient1, 'male')
    add_gender_patient(patient2, 'male')
    print(patient1)
    print(patient2, end="\n\n")

    print("task 18\n")
    add_gender_doctor(doctor1, 'male')
    add_gender_doctor(doctor2, 'male')
    print(doctor1)
    print(doctor2, end="\n\n")