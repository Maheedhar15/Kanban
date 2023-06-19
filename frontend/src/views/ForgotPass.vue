<template>
  <div class="login_page">
    <div class="page">
      <h1 class="welcome">Welcome to Kanban Application</h1>
      <h2 class="logindeets">Enter Details to Reset your password</h2>
      <i class="fa-solid fa-right-to-bracket"></i>
      <div class="loginform">
        <form class="inputform">
          <v-text-field
            class="inputbox1"
            v-model="data.mail"
            :counter="40"
            label="Enter your E-mail ID"
            required
          ></v-text-field>
          <v-text-field
            class="inputbox2"
            v-model="data.password"
            label="Enter New Password"
            required
            type="password"
          ></v-text-field>
          <div class="button">
            <v-btn class="ml-10" @click="onSubmit"> submit </v-btn>
            <v-btn class="ml-6" @click="clear"> clear </v-btn>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from '@vue/reactivity';
import { useRouter } from 'vue-router';
export default {
  name: 'LoginView',
  setup() {
    const router = useRouter();
    const data = reactive({
      mail: '',
      password: '',
    });
    const onSubmit = async () => {
      console.log(data);
      await fetch('http://localhost:5000/forgotpassword', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify(data),
      })
        .then((resp) => resp.json())
        .then((data) => {
          console.log(data);
          alert('Password Changed Successfully');
          router.push('/');
        })
        .catch((error) => {
          if (error) {
            router.push({ name: 'Login' });
            alert('An error has occurred, please try again later');
          }
        });
    };
    const clear = () => {
      (data.mail = ''), (data.password = '');
    };

    return {
      data,
      onSubmit,
      clear,
    };
  },
  data() {
    return {};
  },
};
</script>

<style lang="css" scoped>
.login_page {
  width: 100%;
  min-height: 100vh;
  background: var(--color-bg);
  color: var(--color-primary);
  background-image: url('../assets/bg-texture.png');
}
.welcome {
  text-align: center;
  font-size: 80px;
}

.inputbox1 {
  width: 40%;
  margin-top: 6rem;
}
.inputbox2 {
  width: 40%;
  margin-top: 2rem;
}
.inputform {
  margin-left: 45rem;
}
.button {
  margin-left: 5rem;
  margin-top: 3rem;
}

.logindeets {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 40px;
}
</style>
