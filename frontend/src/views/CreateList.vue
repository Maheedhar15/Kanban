<template>
  <div class="listcreate__page">
    <div class="page">
      <NavBar class="Navbar__createList" :id="`${id}`" />
      <h2 class="listdeets">Create a new list</h2>

      <div class="listcreate__form">
        <form class="inputform">
          <v-text-field
            class="inputbox1"
            v-model="data.l_name"
            :counter="60"
            label="List Name"
            required
          ></v-text-field>

          <div class="button">
            <v-btn class="mr-4 btn__listcreate" @click="onSubmit">
              submit
            </v-btn>
            <v-btn class="mr-4 btn__listcreate" @click="clear"> clear </v-btn>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import { reactive } from 'vue';

export default {
  name: 'createList',
  data() {
    return {
      url: 'http://localhost:5000/createList/' + localStorage['id'],
      id: localStorage['id'],
    };
  },
  setup() {
    const data = reactive({
      l_name: '',
    });
    const onSubmit = async () => {
      console.log(data);
      await fetch('http://localhost:5000/createList/' + localStorage['id'], {
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
          if (data.status == '707') {
            alert('Max NUmber of Lists REached');
          }
        })
        .catch((error) => {
          if (error) {
            if (error.response.status == 401) {
              alert('Your access token was expired');
              this.router.push({ name: 'Login' });
            }
            console.log(error);
          }
        });
    };
    const clear = () => {
      data.l_name = '';
    };

    return {
      data,
      onSubmit,
      clear,
    };
  },
  components: {
    NavBar,
  },
};
</script>

<style scoped>
.listdeets {
  text-align: center;
  margin-top: 4rem;
  font-size: 40px;
  margin-bottom: 10rem;
}
.listcreate__page {
  width: 100%;
  min-height: 100vh;
  background-image: url('../assets/water.jpg');
  background-repeat: no-repeat;
  background-size: cover;
  color: white;
}
.Navbar__createList {
  background-image: url('../assets/water.jpg');
}
.btn__listcreate {
  background: black;
}
.inputform {
  width: 35%;
}
.listcreate__form {
  margin-left: 47rem;
}
.button {
  margin-left: 7rem;
}
</style>
