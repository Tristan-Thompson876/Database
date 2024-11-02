new Vue({
    el: '#app',
    data: {
        username: '',
        password: '',
        isLoggedIn: false,
        courseCode: '',
        courseName: '',
        startDate: '',
        endDate: '',
        //events: []
    },
    methods: {
        registerUser() {
            fetch('http://127.0.0.1:4000/Register', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ Username: this.username, Password: this.password })
            })
            .then(response => response.json())
            .then(data => alert(data.success || data.error));
        },
        loginUser() {
            fetch(`http://127.0.0.1:4000/Userlogin?uname=${this.username}&password=${this.password}`)
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    this.isLoggedIn = true;
                } else {
                    alert(data.error);
                }
            });
        },
        logout() {
            this.isLoggedIn = false;
            this.username = '';
            this.password = '';
        },
        addCourse() {
            fetch('http://127.0.0.1:4000/add_Course', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    CourseC: this.courseCode,
                    CourseName: this.courseName,
                    StartDt: this.startDate,
                    EndDt: this.endDate
                })
            })
            .then(response => response.json())
            .then(data => alert(data.success || data.error));
        },
        /*fetchEvents() {
            fetch('http://127.0.0.1:4000/calendar-events')
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data)) {
                    this.events = data;
                } else {
                    alert(data.error);
                }
            });
        }*/
    }
});
