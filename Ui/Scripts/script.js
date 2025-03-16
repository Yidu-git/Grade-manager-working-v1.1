// grade form
const grade_input = document.getElementById('Score-input')
const grade_submit = document.getElementById('Submit-button')
const subject_input = document.getElementById('Subject-input')
const subject_add_button = document.getElementById('Subject-add-button')
const grade_type_input = document.getElementById('Grade-type-input')

let average = 0

// Aveage form
const calculate_average_button = document.getElementById('Calculate-average-button')
const subject_avg_input = document.getElementById('Average-subject')
const type_avg_input = document.getElementById('Average-type')
const average_rating = document.getElementById('Average-rating')

// Table
const grade_table_body = document.getElementById('table-body')

// Settings
const exit_settings_button = document.getElementById('exit-settings')

// Themes
const Theme = document.getElementById('theme')
const Colorscheme = document.getElementById('Color-scheme')

// -------------- Reset buttons ---------------
// grade
const grade_remove_input = document.getElementById('')
const grade_reset_button = document.getElementById('Reset-Grades')
const grade_remove_button = document.getElementById('Remove-Grade')

// Subject
const subject_reset_button = document.getElementById('Reset-Subjects')
const subject_remove_button = document.getElementById('Remove-Subject')
const subject_remove_input = document.getElementById('Grade-remove-select')

// Reload
const reload_btn = document.getElementById('Reload-button')

// Data-list
const subject_data_list = document.getElementById('Subjets')
const TypeData = document.getElementById('Types')

// Notification
const Notification_popover = document.getElementById('Notification-popover')

function Apply_settings(settings) {
    if (settings != {}) {
        Theme.value = settings['Theme']
        Colorscheme.value = settings['Color-scheme']
    }
}

function notify1(message) {
    Notification_popover.openPopover()
    Notification_popover.innerHTML = message
}

function notify(message) {
    setTimeout(notify1, 3000)
}

function check_rating(score) {
    if (score >= 90) { return 'A' }
    if (score >= 80) { return 'B' }
    if (score >= 70) { return 'C' }
    if (score >= 56) { return 'D' }
    if (score < 56) { return 'F' }
}

function is_fraction(string) {
    if (string.includes('/')) { return true }
}

function check_if_new_subject(subject) {
    eel.read_subjects()(result => {
        if (!result.includes(subject)) {
            eel.add_subject(subject)
            // alert(subject)
            Display_subject(subject)
        }
    })
}

function Display_type(type) {
    let opt = document.createElement('option')
    opt.setAttribute('value', type)
    document.getElementById('Types').appendChild(opt)
}

function Display_types(types) {
    for (let type in types) {
        Display_type(types[type])
        // alert(types[type])
    }
}

function check_if_new_type(type) {
    eel.get_types()(result => {
        if (!result.includes(type)) {
            eel.save_type(type)
            // alert(type)
            Display_type(type)
        }
    })
}

function Display_subject(subject) {
    let option = document.createElement('option')
    option.setAttribute('value', subject)
    document.getElementById('Subjects').appendChild(option)
}

function Display_subjects(subjects) {
    // alert(subjects)
    for (let i = 0; i < subjects.length; i++) {
        Display_subject(subjects[i])
        // alert(subjects[i]) 
    }
}

function RemoveSubjectDisplay(subject) {
    let option = document.querySelector('option[value="' + subject + '"]')
    option.remove()
}

function Remove_All_subject_display() {
    let option = document.createElement('option')
    subject_data_list.replaceChildren(option)
    // subject_data_list.removeChild()
}

// let test = eel.read_subjects()
// alert(test)

// alert('Hi')
// alert(eel.read_subjects())

async function Grade_count() {
    let count = await eel.get_Grade_count()()
    // console.log(count)
    id = id1 + 1
    return count
}

let id1 = 0
function display_grade(subject, grade, type, id) {
    let tr = document.createElement('tr')
    let td_subject = document.createElement('td')
    let td_score = document.createElement('td')
    let td_rating = document.createElement('td')
    let td_remove = document.createElement('td')


    if (id == '') {
        // id = Grade_count()
        // id += 1

        // eel.get_Grade_count()(result => { 
        //     id1 = parseInt(result) + 1
        //     // alert(result)
        //     // alert(id1)
        //     id = id1 + 1
        //     alert(id)
        // })
        // alert(id)

        delete_grades()
        eel.get_grades()(display_all_grades)
        eel.check_gradecount()
    }

    // console.log(id)
    // console.log(id1)


    td_subject.innerText = subject + ' (' + type + ')'
    td_score.innerText = grade

    let check = document.createElement("input")

    check.setAttribute("data-id", id)
    check.setAttribute("class", 'checkbox cancel')
    check.setAttribute("type", "checkbox")
    check.addEventListener("click", (event) => {
        let self_id = event.target.parentElement.parentElement.id.split('.')
        self_id = self_id[1]
        eel.delete_grade(parseInt(self_id))

        event.target.setAttribute("disabled", "true")

        // remove row from table and play animation
        let tr = event.target.parentElement.parentElement
        tr.remove()
        // $(tr).fadeTo("slow",0.001, function(){
        //     $(this).remove();
        // })

    });

    td_remove.appendChild(check)

    // Checking if grade is fraction or out of a hundred
    if (is_fraction(grade)) {
        let value = grade.split('/')[0]
        let total = grade.split('/')[1]
        // alert(String(value,total))
        grade = parseFloat(value) / parseFloat(total) * 100
    }

    let rating = check_rating(parseFloat(grade))
    td_rating.innerText = rating
    td_rating.setAttribute('class', rating)

    tr.appendChild(td_subject)
    tr.appendChild(td_score)
    tr.appendChild(td_rating)
    tr.appendChild(td_remove)

    tr.setAttribute('id', 'grade' + '.' + id)
    grade_table_body.appendChild(tr)
}

function display_all_grades(grades) {
    for (let grade of grades['Grades']) {
        display_grade(grade['Subject'], grade['Grade'], grade['Type'], grade['id'])
    }
}

function show_grade() {
    let grade = grade_input.value
    let subject = subject_input.value
    let type = grade_type_input.value

    display_grade(subject, grade, type, '')

    grade_input.value = ''
    subject_input.value = ''

    eel.save_grade(subject, grade, type)
}

function delete_grades() {
    let grades = document.querySelectorAll('*[id^= "grade"')
    for (let i = 0; i < grades.length; i++) {
        grades.item(i).remove()
    }
}

function calculate_average(value) {
    average = value
    // alert(average)
}

// alert(eel.return_test()(result => { return() => result}))

grade_submit.addEventListener("click", (event) => {
    check_if_new_subject(subject_input.value)
    check_if_new_type(grade_type_input.value)
    show_grade()
    // eel.print_test()
})

grade_reset_button.addEventListener("click", (event) => {
    // eel.print_test()
    eel.reset_grades()
    delete_grades()
})

calculate_average_button.addEventListener("click", (event) => {
    let label = document.getElementById('Average-label')
    if (subject_avg_input.value == 'All' | subject_avg_input.value == 'ALL' | subject_avg_input == 'all' | subject_avg_input == '') { eel.get_grades_average()(calculate_average) }
    else { eel.get_average(subject_avg_input.value, type_avg_input.value)(calculate_average) }

    label.innerHTML = 'Average : ' + average
    average_rating.setAttribute('class', check_rating(average))
    average_rating.innerHTML = check_rating(average)
})

subject_reset_button.addEventListener("click", (event) => {
    // alert('Subjects have been reset')
    eel.reset_subjects()
    Remove_All_subject_display()
    // notify('Hello')
})

exit_settings_button.addEventListener('click', (event) => {
    eel.save_settings(Theme.value, Colorscheme.value)
})

// Subject removal
subject_remove_button.addEventListener('click', (event) => {
    eel.remove_subject(subject_remove_input.value)
    // alert(subject_remove_input.value + 'Has been removed from subjects')
    RemoveSubjectDisplay(subject_remove_input.value)
})

subject_add_button.addEventListener('click', (event) => {
    eel.add_subject(subject_input.value)
    Display_subject(subject_input.value)
})

reload_btn.addEventListener('click', (event) => {
    // Remove_All_subject_display()
    delete_grades()
    // alert('Hello')

    eel.check_gradecount()
    eel.get_settings()(Apply_settings)
    // eel.read_subjects()(Display_subjects)
    eel.get_grades()(display_all_grades)
})

eel.get_types()(Display_types)
eel.get_settings()(Apply_settings)
eel.read_subjects()(Display_subjects)
eel.get_grades()(display_all_grades)