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
            <input
              v-model="resetEmail"
              type="email"
              placeholder="Enter your email to reset password"
              required
            />
            <div v-if="!resetApproved">
              <button
                @click="sendResendEmail"
                type="submit"
                :disabled="!resetEmail.includes('@')"
                :class="{ 'disabled-btn': !resetEmail.includes('@') }"
                this.codes=""
              >
                Send Reset Code
              </button>
              <div v-if="loading" class="p-loader">
                <div class="loader"></div>
              </div>

              <p id="password_resetInfo">{{ resetMessage }}</p>

              <div id="six-digit-codeInput">
                <input
                  v-for="(code, index) in codes"
                  :key="index"
                  v-model="codes[index]"
                  :id="'digit' + (index + 1)"
                  :class="{ diggitLoader: verifyCodeloading }"
                  type="text"
                  maxlength="1"
                  pattern="[0-9]"
                  @input="moveNext($event, index)"
                  @paste.prevent
                  @keydown="preventInvalidInput($event)"
                />
              </div>
            </div>

            <div v-if="resetApproved" id="resetPasswordInput">
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
import {
  SIGN_UP,
  SEND_EMAIL_RESET_CODES,
  VERIFY_CODES,
  AUTH_WITH_GOOGLE,
  MANUAL_LOGIN,
} from "@/utils";

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
      verifyCodeloading: false,
      message: "",
      success: false,
      isLogin: true,
      isSignup: false,
      isResetPassword: false,
      resetEmail: "",
      resetMessage: "Enter you Email to get password reset codes.",
      codes: ["", "", "", "", "", ""],
      resetApproved: false,
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
      this.checkAndVerify();
    },
    preventInvalidInput(event) {
      if (event.target.value.length >= 1 && event.key !== "Backspace") {
        event.preventDefault();
      }
    },

    checkAndVerify() {
      if (this.codes.every((code) => code.length === 1)) {
        this.verifyCode();
      } else {
        const emptyIndex = this.codes.findIndex((code) => code === "");
        if (emptyIndex !== -1) {
          document.getElementById("digit" + (emptyIndex + 1))?.focus();
        }
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
    async sendResendEmail() {
      if (!this.resetEmail) {
        this.showMessage("Email is missing !!", false);
        return;
      }

      this.loading = true;

      try {
        const response = await axios.post(SEND_EMAIL_RESET_CODES, {
          email: this.resetEmail,
        });

        console.log(response.data);
        this.resetMessage = response.data.error
          ? response.data.error
          : response.data.message;
        this.showMessage("Enter Codes sent to your Email", true);
      } catch (error) {
        console.error("Email resend error:", error);

        this.resetMessage = error.response.data.error
          ? error.response.data.error
          : error.response.data.message;

        this.showMessage(this.resetMessage, false);
      } finally {
        this.loading = false;
      }
    },

    async verifyCode() {
      console.log("Verifying:", this.codes.join(""));

      if (!this.resetEmail || !this.codes.join("")) {
        this.showMessage("Please fill in all fields!", false);
        return;
      }

      this.verifyCodeloading = true;

      try {
        const response = await axios.post(VERIFY_CODES, {
          email: this.resetEmail,
          code: this.codes.join(""),
        });

        console.log("Verification Response:", response.data);

        if (response.data.success) {
          this.resetApproved = true;
          this.showMessage("Code verified! You can now reset your password.", true);
        } else {
          this.showMessage(response.data.message || "Invalid code. Try again.", false);
        }
      } catch (error) {
        console.error("Verification error:", error);
        this.showMessage(
          error.response?.data?.error || "Verification failed. Try again.",
          false
        );
      }
       finally {
        this.verifyCodeloading = false; 
      }
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
.disabled-btn:hover {
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
  padding: 5px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  box-sizing: border-box;
  background: #4b484843;
}
#resetPassword p {
  color: #000000;
  font-weight: bold;
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
  gap: 5px;
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
  background: rgba(0, 0, 0, 0.751);
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
.close-btn:hover {
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
  background-color: rgb(209, 209, 209);
  box-shadow: 0px 0px 10px black !important;
  filter: drop-shadow(0px 0px 5px rgb(0, 0, 0));
  align-items: center;
}

#password_resetInfo {
  font-size: 14px;
  color: #e7dcdc !important;
}

.diggitLoader {
  width: 15px;
  height: 15px;
  border-radius: 50% !important;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  font-size: 14px;
  text-align: center;
  line-height: 15px;
  border-radius: 3px;
  animation: bounce 1.2s infinite ease-in-out;
}

.diggitLoader:nth-child(1) {
  animation-delay: 0s;
}
.diggitLoader:nth-child(2) {
  animation-delay: 0.2s;
}
.diggitLoader:nth-child(3) {
  animation-delay: 0.4s;
}
.diggitLoader:nth-child(4) {
  animation-delay: 0.6s;
}
.diggitLoader:nth-child(5) {
  animation-delay: 0.8s;
}
.diggitLoader:nth-child(6) {
  animation-delay: 1s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
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
