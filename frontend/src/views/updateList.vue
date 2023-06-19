<template>
  <div class="listcreate__page">
    <div class="page">
      <NavBar class="Navbar__createList" :id="`${id}`" />
      <h2 class="listdeets">Update your list</h2>
      <div class="listcreate__form">
        <form class="inputform">
          <v-text-field
            class="inputbox1"
            v-model="updated_list_name"
            :counter="60"
            :label="`${list_name}`"
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
import { useRouter } from 'vue-router';
import axios from 'axios';
export default {
  name: 'updateList',
  data() {
    return {
      url: 'http://localhost:5000/updateList/' + this.$route.params.lid,
      list_name: '',
      updated_list_name: '',
      router: useRouter(),
      id: localStorage['id'],
    };
  },
  setup() {
    const data = reactive({
      l_name: '',
    });

    const clear = () => {
      data.l_name = '';
    };

    return {
      data,
      clear,
    };
  },
  methods: {
    onSubmit() {
      console.log(this.updated_list_name);
      fetch('http://localhost:5000/updateList/' + this.$route.params.lid, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({ l_name: this.updated_list_name }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          console.log(data);
          this.router.push('/dashboard/' + localStorage['id']);
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
    },
    getList() {
      const path = 'http://localhost:5000/updateList/' + this.$route.params.lid;
      axios
        .get(path)
        .then((res) => {
          this.list_name = res.data.list['list_name'];
        })

        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    this.getList();
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
