<template>
  <div class="listcreate__page">
    <div class="page">
      <NavBar class="Navbar__createList" :id="`${id}`" />
      <h2 class="listdeets">Create a new task</h2>

      <div class="listcreate__form">
        <form class="inputform">
          <v-select
            v-model="activeList"
            class="ListSelect"
            :items="availableLists"
          >
          </v-select>
          <v-text-field
            class="inputbox1"
            v-model="data.title"
            :counter="40"
            label="Title"
            required
          >
          </v-text-field>

          <v-text-field
            class="inputbox1"
            v-model="data.description"
            :counter="200"
            label="Description"
            required
          >
          </v-text-field>
          <v-switch
            v-model="data.isComplete"
            :label="`Mark as Complete`"
            class="switch"
          ></v-switch>
          <div class="button">
            <v-btn class="mr-4 btn__listcreate" @click="onSubmit">
              submit
            </v-btn>
            <v-btn class="mr-4 btn__listcreate" @click="clear"> clear </v-btn>
          </div>
        </form>
        <form class="Datepicker">
          <small>Pick a Deadline</small>
          <div class="date">
            <v-text-field class="desc-cal">
              <dp v-model="data.deadline" :flow="flow" modeHeight="120" />
            </v-text-field>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import { ref } from 'vue';
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
export default {
  name: 'updateTask',
  data() {
    return {
      url: 'http://localhost:5000/createTask/' + localStorage['id'],
      activeListID: this.$route.params.lid,
      activeList: '',
      availableLists: [],
      router: useRouter(),
      id: localStorage['id'],
    };
  },
  setup() {
    const data = reactive({
      title: '',
      description: '',
      isComplete: false,
      deadline: new Date(),
    });
    const flow = ref(['month', 'year', 'calendar']);
    const submit = () => {
      console.log(data);
    };
    const clear = () => {
      data.l_name = '';
    };

    return {
      data,
      clear,
      submit,
      flow,
    };
  },
  components: {
    NavBar,
  },
  methods: {
    getLists() {
      const path = this.url;
      const token = localStorage['access_token'];
      axios
        .get(path, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          console.log(res.data.availableLists);
          for (let i = 0; i < res.data.availableLists.length; i++) {
            if (this.activeListID == res.data.availableLists[i]['list_id']) {
              this.activeList = res.data.availableLists[i]['list_name'];
            }
            this.availableLists.push(res.data.availableLists[i]['list_name']);
          }
          console.log(this.availableLists);
        })
        .catch((err) => {
          if (err.response.status == 401) {
            alert('Your access token was expired');
            this.router.push({ name: 'Login' });
          }
          console.log(err);
        });
    },
    onSubmit() {
      console.log(this.data);
      axios
        .post('http://localhost:5000/createTask/' + localStorage['id'], {
          list_name: this.activeList,
          task_title: this.data.title,
          task_desc: this.data.description,
          status: this.data.isComplete,
          deadline: this.data.deadline,
        })
        .then((resp) => {
          console.log(resp.data);
          this.router.push('/dashboard/' + localStorage['id']);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    itemClicked() {
      this.toggleMenu();
    },
  },
  mounted() {
    this.getLists();
  },
};
</script>

<style scoped>
.listdeets {
  text-align: center;
  margin-top: 2rem;
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
  margin-top: -2rem;
}
.button {
  margin-left: 7rem;
}
.ListSelect {
  width: 400px;
  text-align: center;
}
.switch {
  color: orange;
}
.Datepicker {
  margin-left: 35rem;
  width: 35%;
  margin-top: -23rem;
}
</style>
