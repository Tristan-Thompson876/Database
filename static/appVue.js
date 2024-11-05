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
        async registerUser() {
            try {
                const response = await fetch(`http://127.0.0.1:4000/Userlogin?uname=${this.username}&password=${this.password}`);
                const data = await response.json();
                if (data.message) {
                    this.isLoggedIn = true;
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Login failed. Please try again.');
            }
        },
        loginUser() {
            // Simulate login success
            if (this.username && this.password) {
                this.isLoggedIn = true;
            } else {
                alert('Please enter valid credentials.');
            }
        },
        logout() {
            this.isLoggedIn = false;
            this.username = '';
            this.password = '';
        },
        async addCourse() {
            try {
                const response = await fetch('http://127.0.0.1:4000/add_Course', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        CourseC: this.courseCode,
                        CourseName: this.courseName,
                        StartDt: this.startDate,
                        EndDt: this.endDate
                    })
                });
                const data = await response.json();
                alert(data.success || data.error);
            } catch (error) {
                console.error('Error adding course:', error);
                alert('Failed to add course. Please try again.');
            }
        }
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
