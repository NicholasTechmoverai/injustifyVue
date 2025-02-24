<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <!-- Close Button -->
      <button class="close-btn" @click="closeModal">✖</button>

      <!-- Login Form -->
      <div v-if="isLogin">
        <h1 class="injustifyLogoR">
          <ion-icon name="musical-note-outline"></ion-icon>Injustify
          <ion-icon name="musical-note-outline"></ion-icon>
        </h1>
        <div id="logininjustify">
          <h2>Login</h2>
          <form @submit.prevent="login">
            <input v-model="userEmail" type="email" placeholder="Email" required />
            <div class="passwordInputs">
              <input
                v-model="userPassword"
                type="password"
                placeholder="Password"
                required
              />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <button type="submit">Login</button>
            <div v-if="loading" class="p-loader">
              <div class="loader"></div>
            </div>
            <label>
              <input type="checkbox" v-model="rememberMe" />
              Remember Me
            </label>
          </form>
          <div class="googleLogin" @click="authWithGoogle">
            <span>Login with;</span>
            <img src="../assets/google_logo.png" alt="Google Logo" />
          </div>
          <p>
            Forgot Password?
            <a href="#" @click="switchMode('resetPassword')">Reset Password</a>
          </p>
          <p>Don't have an account? <a @click="switchMode('signup')">Sign up</a></p>
        </div>
      </div>

      <!-- Signup Form -->
      <div v-if="isSignup">
        <h1 class="injustifyLogoR">
          <ion-icon name="musical-note-outline"></ion-icon>Injustify
          <ion-icon name="musical-note-outline"></ion-icon>
        </h1>
        <div id="signupinjustify">
          <h2>Sign Up</h2>
          <form @submit.prevent="signup">
            <input v-model="signupEmail" type="email" placeholder="Email" required />
            <input v-model="signupUsername" type="text" placeholder="Username" required />
            <div class="passwordInputs">
              <input
                v-model="signupPassword"
                type="password"
                placeholder="Password"
                required
              />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <div class="passwordInputs">
              <input
                v-model="signupConfirmPassword"
                type="password"
                placeholder="Confirm Password"
                required
              />
              <div class="showHidePassword" @click="togglePasswordVisibility">
                <i class="fa-solid fa-eye"></i>
              </div>
            </div>
            <button type="submit">Sign Up</button>
            <div v-if="loading" class="p-loader">
              <div class="loader"></div>
            </div>
          </form>
          <div class="googleLogin" @click="authWithGoogle">
            <span>Signup with;</span>
            <img src="../assets/google_logo.png" alt="Google Logo" />
          </div>
          <label>
            <input type="checkbox" v-model="termsAccepted" required />
            I agree to the <a href="#">Terms and Conditions</a>
          </label>
          <p>Already have an account? <a @click="switchMode('islogin')">Login</a></p>
        </div>
      </div>
      <div v-if="isResetPassword" id="resetPassword">
        <h1 class="injustifyLogoR">
          <ion-icon name="musical-note-outline"></ion-icon>Injustify
          <ion-icon name="musical-note-outline"></ion-icon>
        </h1>

        <div>
          <h2>Reset Password</h2>
          <form @submit.prevent="resetPassword">
            <input v-model="resetEmail" type="email" placeholder="Enter Email you to seset password" required />
            <button type="submit" :disabled="!resetEmail.includes('@')"  :class="{ 'disabled-btn':!resetEmail.includes('@')}">Send Reset Code</button>
            <div v-if="loading" class="p-loader">
              <div class="loader"></div>
            </div>

            <p>Check your email for a 6-digit reset code.</p>

            <div id="six-digit-codeInput">
              <input
                v-model="CheckCode1"
                id="digit1"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @input="moveNext($event, 'digit2')"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />

              <input
                v-model="CheckCode2"
                id="digit2"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @input="moveNext($event, 'digit3')"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />

              <input
                v-model="CheckCode3"
                id="digit3"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @input="moveNext($event, 'digit4')"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />

              <input
                v-model="CheckCode4"
                id="digit4"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @input="moveNext($event, 'digit5')"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />

              <input
                v-model="CheckCode5"
                id="digit5"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @input="moveNext($event, 'digit6')"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />

              <input
                v-model="CheckCode6"
                id="digit6"
                type="text"
                maxlength="1"
                pattern="[0-9]"
                @paste.prevent
                @keydown="
                  (e) =>
                    e.target.value.length >= 1 && e.key !== 'Backspace'
                      ? e.preventDefault()
                      : null
                "
                oninput="this.value = this.value.replace(/[^0-9]/g, '')"
              />
            </div>

            <p>Back to <a @click.prevent="switchMode('login')">Login</a></p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/store";
import { SIGN_UP, AUTH_WITH_GOOGLE, MANUAL_LOGIN } from "@/utils";

export default {
  props: {
    isOpen: Boolean,
    onCloseModal: Function,
    isDarkMode: Boolean,
  },
  data() {
    return {
      userEmail: "",
      userPassword: "",
      signupEmail: "",
      signupUsername: "",
      signupPassword: "",
      signupConfirmPassword: "",
      rememberMe: false,
      termsAccepted: false,
      loading: false,
      message: "",
      success: false,
      isLogin: true,
      isSignup: false,
      isResetPassword: false,
      resetEmail: "",
      CheckCodes: "",      
    };
  },
  methods: {
    authWithGoogle() {
      window.location.href = AUTH_WITH_GOOGLE;
    },
    isValidEmail() {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.resetEmail);
  },
    moveNext(event, nextId) {
      const input = event.target;

      // Ensure only one digit is entered
      input.value = input.value.replace(/[^0-9]/g, "").slice(0, 1);

      if (input.value.length === 1 && nextId) {
        document.getElementById(nextId)?.focus();
      }
    },

    async login() {
      if (!this.userEmail || !this.userPassword) {
        this.showMessage("Please fill in all fields!", false);
        return;
      }

      this.loading = true;
      try {
        const response = await axios.post(MANUAL_LOGIN, {
          email: this.userEmail,
          password: this.userPassword,
        });

        this.showMessage("Login successful!", true);
        if (response.data.user) {
          const userStore = useUserStore();
          userStore.setUser(response.data.user);
          this.loading = false;
        }

        console.log("Backend response:", response.data);
        this.closeModal();
      } catch (error) {
        this.showMessage("Login failed. Check your credentials.", false);
        console.error("Login error:", error);
      }
      this.loading = false;
    },

    async signup() {
      if (
        !this.signupEmail ||
        !this.signupUsername ||
        !this.signupPassword ||
        !this.signupConfirmPassword
      ) {
        this.showMessage("Please fill in all fields!", false);
        return;
      }

      if (this.signupPassword !== this.signupConfirmPassword) {
        this.showMessage("Passwords do not match!", false);
        return;
      }

      this.loading = true;
      try {
        const response = await axios.post(SIGN_UP, {
          email: this.signupEmail,
          username: this.signupUsername,
          password: this.signupPassword,
        });

        this.showMessage("Signup successful!", true);
        if (response.data.user) {
          const userStore = useUserStore();
          userStore.setUser(response.data.user);
          this.loading = false;
        }

        console.log("Backend response:", response.data);
        this.closeModal();
      } catch (error) {
        this.showMessage("Signup failed. Try again.", false);
        console.error("Signup error:", error);
      }
      this.loading = false;
    },

    switchMode(v) {
      if (v == "signup") {
        this.isSignup = true;
        this.isLogin = false;
        this.isResetPassword = false;
      } else if (v == "logoin") {
        this.isSignup = false;
        this.isLogin = true;
        this.isResetPassword = false;
      } else if (v == "resetPassword") {
        this.isSignup = false;
        this.isLogin = false;
        this.isResetPassword = true;
      } else {
        this.isSignup = false;
        this.isLogin = true;
        this.isResetPassword = false;
      }
    },

    closeModal() {
      console.log("Close modal button clicked");
      this.$emit("close");
    },

    showMessage(message, success) {
      this.message = message;
      this.success = success;
    },
    togglePasswordVisibility(event) {
      let inputField = event.target.closest(".passwordInputs").querySelector("input");
      inputField.type = inputField.type === "password" ? "text" : "password";
    },
  },
};
</script>

<style scoped>
/* General Styles */
.disabled-btn {
  background: #ccc;
  cursor: not-allowed;
}
.disabled-btn:hover{
  background: #ccc !important;
}
.active-btn {
  background: #007bff;
  cursor: pointer;
}

.active-btn:hover {
  background: #0056b3;
}

#resetPassword {
  width: 100%;
  margin: 10px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  box-sizing: border-box;
  background: #4b484843;
}

.injustifyLogoR {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
  top: 0;
  left: 1px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

input[type="email"],
input[type="number"],
input[type="password"],
input[type="text"] {
  font-size: 16px;
  text-align: center;
}

button,
.modal-btn {
  padding: 10px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
  width: 100%;
}

button:hover,
.modal-btn:hover {
  background: #0056b3;
}

p {
  font-size: 14px;
  color: #666;
}

p a,
.switch-text a {
  color: #007bff;
  cursor: pointer;
  text-decoration: none;
  font-weight: bold;
}

p a:hover,
.switch-text a:hover {
  text-decoration: underline;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-container {
  background-image: url(../assets/outerSpaceTerrain.jpg);
  padding: 25px;
  border-radius: 10px;
  width: 350px;
  text-align: center;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  opacity: 1;
  transform: translateY(0);
  color: white !important;
  background-size: cover;
  animation: slideIn 0.5s ease-in-out;

}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover{
  background: #51171749;
}
.modal-title {
  font-size: 24px;
  margin-bottom: 15px;
  color: #333;
}

.switch-text {
  margin-top: 10px;
}

/* Loader */
.p-loader {
  display: flex;
  justify-content: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: white;
  align-items: center;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}




@keyframes slideIn {
  from {
    transform: translateY(-25px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Code Input */
#six-digit-codeInput {
  display: flex;
  justify-content: center;
  gap: 10px;
}

#six-digit-codeInput input {
  width: 40px;
  height: 40px;
  font-size: 20px;
  text-align: center;
  border: 2px solid #007bff;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s;
}

#six-digit-codeInput input:focus {
  border-color: #0478f4;
  background-color: #333;
}

/* Password Inputs */
.passwordInputs {
  position: relative;
  width: 100%;
}

.passwordInputs .showHidePassword {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  cursor: pointer;
  color: gray;
  padding: 3px 2px;
}

.passwordInputs .showHidePassword:hover {
  color: rgb(40, 35, 35);
}

.passwordInputs input[type="password"] {
  padding-right: 40px !important;
}

/* Google Login */
.googleLogin img {
  width: 100px;
  border-radius: 10px;
  cursor: pointer;
}

.googleLogin img:hover {
  background-color: rgba(128, 128, 128, 0.115);
}
</style>
