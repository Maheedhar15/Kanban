<template>
  <div class="login_page">
    <div class="page">
      <h1 class="welcome">Welcome to Kanban Application</h1>
      <fa class="icon" icon="fa-solid fa-right-to-bracket" />
      <h2 class="logindeets">Enter your Login Details</h2>
      <i class="fa-solid fa-right-to-bracket"></i>
      <div class="loginform">
        <form class="inputform">
          <v-text-field
            class="inputbox1"
            v-model="data.mail"
            :counter="40"
            label="E-mail ID"
            required
          ></v-text-field>
          <v-text-field
            class="inputbox2"
            v-model="data.password"
            label="password"
            required
            type="password"
          ></v-text-field>
          <div class="button">
            <v-btn class="mr-4" @click="onSubmit"> submit </v-btn>
            <v-btn class="mr-4" @click="clear"> clear </v-btn>
            <v-btn @click="reg">Register</v-btn>
            <br />
            <v-btn class="mr-4 mt-2 ml-15" @click="forgot">
              Forgot Password?</v-btn
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mdiLogin } from '@mdi/js';
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
      await fetch('http://localhost:5000/login', {
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
          localStorage.setItem('access_token', data['access_token']);
          localStorage.setItem('id', data['id']);
          localStorage.setItem('name', data['name']);

          router.push('/dashboard/' + data['id']);
        })
        .catch((error) => {
          if (error) {
            router.push({ name: 'Login' });
            alert('Wrong Password, Please try again');
          }
        });
    };
    const clear = () => {
      (data.mail = ''), (data.password = '');
    };

    const reg = async () => {
      await router.push('/register');
    };

    const forgot = async () => {
      await router.push('/forgotpassword');
    };

    return {
      data,
      onSubmit,
      clear,
      reg,
      forgot,
    };
  },
  data() {
    return {
      mdiLogin,
    };
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
.icon {
  margin-left: 58rem;
  margin-top: 1.5rem;
  height: 40px;
  width: 40px;
}
</style>
