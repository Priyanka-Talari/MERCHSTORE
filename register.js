document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded!");

    const auth = window.firebaseAuth;
    const db = window.firestoreDB; // Ensure Firestore is initialized correctly

    // 🔹 Toggle Login & Register Forms
    window.toggleForm = function () {
        let registerForm = document.getElementById("register");
        let loginForm = document.getElementById("login");

        registerForm.style.display = registerForm.style.display === "none" ? "block" : "none";
        loginForm.style.display = loginForm.style.display === "none" ? "block" : "none";
    };

    // 🔹 Show/Hide Password
    window.togglePassword = function (id) {
        let passwordField = document.getElementById(id);
        let eyeIcon = passwordField.nextElementSibling;

        passwordField.type = passwordField.type === "password" ? "text" : "password";
        eyeIcon.innerText = passwordField.type === "password" ? "👀" : "🙈";
    };

    // 🔹 Register User & Store in Firestore
    window.register = async function () {
        let email = document.getElementById("email").value.trim();
        let password = document.getElementById("password").value.trim();
        let confirmPassword = document.getElementById("confirmPassword").value.trim();

        if (password.length < 6 || !/[A-Z]/.test(password) || !/\d/.test(password) || password !== confirmPassword) {
            alert("❌ Password must be at least 6 characters, contain an uppercase letter, a number, and match confirm password.");
            return;
        }

        try {
            // ✅ Register User in Firebase Auth
            const { createUserWithEmailAndPassword } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js");
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            // ✅ Store user info in Firestore `users` collection
            const { collection, setDoc, doc } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js");
            await setDoc(doc(collection(db, "users"), user.uid), {
                email: email,
                createdAt: new Date(),
                uid: user.uid // Store UID for easier debugging
            });

            alert("✅ Registered successfully! Redirecting to login...");

            // ✅ Reset form fields
            document.getElementById("email").value = "";
            document.getElementById("password").value = "";
            document.getElementById("confirmPassword").value = "";

            // ✅ Automatically switch to login form
            toggleForm();
        } catch (error) {
            console.error("🔥 Registration Error:", error);
            alert(`❌ Registration failed: ${error.message}`);
        }
    };

    // 🔹 Login User & Check Firestore
    window.login = async function () {
        let email = document.getElementById("loginEmail").value.trim();
        let password = document.getElementById("loginPassword").value.trim();

        try {
            // ✅ Sign in User
            const { signInWithEmailAndPassword } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js");
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            // ✅ Check if user is an admin in Firestore
            const { collection, query, where, getDocs } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js");
            const adminsRef = collection(db, "admins");
            const q = query(adminsRef, where("email", "==", email));
            const querySnapshot = await getDocs(q);

            if (!querySnapshot.empty) {
                alert("✅ Admin login successful!");
                window.location.href = "admin-dashboard.html"; // Redirect admin
            } else {
                alert("✅ User login successful!");
                window.location.href = "index.html"; // Redirect user
            }
        } catch (error) {
            console.error("🔥 Login Error:", error);
            alert(`❌ Login failed: ${error.message}`);
        }
    };

    console.log("✅ Event listeners set up successfully.");
});
