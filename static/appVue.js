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
    },
    methods: {
        // Method to handle user login
        async loginUser() {
            if (!this.username || !this.password) {
                alert('Please enter both username and password.');
                return;
            }
            try {
                const response = await fetch('http://127.0.0.1:4000/Userlogin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        uname: this.username,
                        password: this.password
                    })
                });

                const data = await response.json();
                if (response.ok) {
                    this.isLoggedIn = true; // Login successful
                    alert(data.message);
                } else {
                    alert(data.error || 'Login failed.');
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Login failed. Please try again.');
            }
        },

        // Method to handle user logout
        logout() {
            this.isLoggedIn = false;
            this.username = '';
            this.password = '';
            alert('You have been logged out.');
        },

        // Method to add a new course
        async addCourse() {
            if (!this.courseCode || !this.courseName || !this.startDate || !this.endDate) {
                alert('Please fill in all course details.');
                return;
            }
            try {
                const response = await fetch('http://127.0.0.1:4000/add_Course', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        CourseC: this.courseCode,
                        CourseName: this.courseName,
                        StartDt: this.startDate,
                        EndDt: this.endDate
                    })
                });
                const data = await response.json();

                if (response.ok) {
                    alert(data.success);
                } else {
                    alert(data.error || 'Failed to add course.');
                }
            } catch (error) {
                console.error('Error adding course:', error);
                alert('Failed to add course. Please try again.');
            }
        },

        // Navigation logic (if needed)
        goToPage(page) {
            alert(`Navigating to ${page}`);
        }
    }
});
