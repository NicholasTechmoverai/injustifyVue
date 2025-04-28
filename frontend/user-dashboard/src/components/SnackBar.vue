<template>
  <div>
    <div id="snackbar-container">
      <div
        v-for="(snackbar, index) in snackbars"
        :key="index"
        :class="['snackbar', snackbar.type]"
      >
        <span class="snackbarcontent">
          <ion-icon :name="icons[snackbar.type]"></ion-icon> {{ snackbar.message }}
        </span>
        <button class="close-btn" @click="removeSnackbar(index)">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useUserStore } from "@/store/index.js";

export default {
  data() {
    const userStore = useUserStore();

    return {
      snackbars: computed(() => userStore.SnackBar_messages),
      icons: {
        success: "checkmark-circle",
        error: "alert-circle",
        info: "information-circle",
      },
    };
  },
  methods: {
    showSnackbar(message, type = "info") {
      this.snackbars.push({ message, type });

      // Auto-remove after 4.5 seconds
      setTimeout(() => {
        this.snackbars.shift();
      }, 10000);
    },
    removeSnackbar(index) {
      this.snackbars.splice(index, 1);
    },
  },
};
</script>

<style scoped>
/* Snackbar container */
#snackbar-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000;
}

/* Snackbar styles */
.snackbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 280px;
  max-width: 420px;
  padding: 15px;
  border-radius: 12px;
  color: rgb(235, 231, 231);
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.5s ease, fadeOut 0.5s ease 7s forwards;
  position: relative;
  opacity: 0.9;
}
.snackbarcontent {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-direction: row;
}
.snackbarcontent ion-icon {
  color: rgb(225, 220, 220);
  font-weight: bolder;
  font-size: 20px !important;
}
/* Snackbar types */
.snackbar.error {
  background-color: #e74c3c;
}
.snackbar.info {
  background-color: #3498db;
}
.snackbar.success {
  background-color: #2ecc71;
}

/* Icons */
.snackbar i {
  margin-right: 10px;
  font-size: 20px;
}

/* Close button */
.snackbar .close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-left: 15px;
}

/* Animations */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 0.9;
  }
}

@keyframes fadeOut {
  from {
    opacity: 0.9;
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}
</style>
