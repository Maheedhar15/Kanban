<template>
  <div class="dashboard">
    <Navbar class="navbar__dash" :id="`${id}`" />
    <h1 class="dashboard__welcome">Welcome {{ name }}</h1>
    <div class="listview">
      <div class="no__lists" v-if="len_list === 0">
        <h2 class="no_lists">There are No lists here tap to add</h2>
      </div>
      <div class="has__lists" v-else>
        <div class="all__lists" v-for="(item, index) in items" :key="index">
          <div class="list">
            <div class="title">
              <div class="title__options">
                <h1 class="list_name">{{ item[0].list_name }}</h1>
                <Dropdown :id="`${item[0].list_id}`" />
                <!-- V-menu -->
                <!--menu ends-->
              </div>
            </div>
            <div class="body">
              <div class="no_tasks" v-if="item[0].no_of_tasks === 0">
                <h3 class="headline__dash">There are no tasks added yet</h3>
                <router-link
                  class="createList"
                  :to="`/createTask/${id}/${item[0].list_id}`"
                >
                  <fa class="list_plus" icon="fa-solid fa-plus" />
                </router-link>
              </div>
              <div class="has_tasks" v-else>
                <h4 class="headline__dash">Here are your tasks</h4>

                <div
                  class="tasksforthis"
                  v-for="(task, index1) in item[1]"
                  :key="index1"
                >
                  <div
                    class="filtered__tasks"
                    v-if:="`{{ item[0].list_id }} == {{ task.list_id }}`"
                  >
                    <div class="task__ui">
                      <div class="task_title_options">
                        <header class="task__title">{{ task.title }}</header>
                        <DropdownT
                          :id="`${task.task_id}`"
                          class="task__dropdown"
                        />
                      </div>
                      <p>{{ task.desc }}</p>
                      <br />
                      <p class="deadline">Deadline: {{ task.deadline }}</p>
                      <DropdownM
                        class="dropdown_m"
                        :tid="`${task.task_id}`"
                        :items="availableLists"
                      />
                    </div>
                  </div>
                </div>
                <router-link
                  class="createList"
                  :to="`/createTask/${id}/${item[0].list_id}`"
                >
                  <fa class="list_plus" icon="fa-solid fa-plus" />
                </router-link>
              </div>
            </div>
            <div class="footer">
              <v-btn elevation="9" outlined class="exportbtn">
                <a
                  :href="`http://localhost:5000/export_list/${item[0].list_id}`"
                  class="export_task"
                  >Export
                </a>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
      <router-link :to="`/createList/${id}`">
        <fa class="plus__icon" icon="fa-solid fa-plus" />
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Dropdown from '@/components/DropdownList.vue';
import Navbar from '../components/NavBar.vue';
import DropdownT from '../components/DropdownTask.vue';
import DropdownM from '../components/DropDownMove.vue';
import { useRouter } from 'vue-router';
export default {
  name: 'DashboardView',
  data() {
    return {
      name: localStorage['name'],
      len_list: 0,
      items: [],
      id: localStorage['id'],
      router: useRouter(),
      availableLists: [],
    };
  },
  methods: {
    getTrackers() {
      const token = localStorage['access_token'];
      const path = 'http://localhost:5000/dashboard/' + this.$route.params.id;
      axios
        .get(path, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.items = res.data.list;
          this.availableLists = res.data.availableLists;
          this.len_list = res.data.list[0][0]['len_list'];
          console.log(res.data.list);
        })

        .catch((err) => {
          if (err.response.status == 401) {
            alert('Your access token was expired');
            this.router.push({ name: 'Login' });
          }
          console.log(err);
        });

      console.log(this.items);
    },
  },
  components: {
    Navbar,
    Dropdown,
    DropdownT,
    DropdownM,
  },
  created() {
    this.getTrackers();
  },
};
</script>

<style>
.dashboard {
  width: 100%;
  min-height: 100vh;
  color: #8a2be2;
  background-image: url('../assets/black-purple.jpg');
  background-repeat: repeat-y;
  overflow-x: auto;
  overflow-y: hidden;
}
.dashboard__welcome {
  margin-top: 2rem;
  font-weight: 600;
  margin-left: 2rem;
}
.plus__icon {
  margin-left: 58rem;
  width: 32px;
  height: 32px;
  margin-top: 1rem;
  color: white;
  padding: 1rem;
  border: 1px solid white;
  border-radius: 50%;
  transition: var(--transition);
}
.plus__icon:hover {
  background: black;
  color: #8a2be2;
  border: 1px solid #8a2be2;
}
.no_lists {
  text-align: center;
  margin-top: 15rem;
}

.navbar__dash {
  background-color: black;
  color: white;
  max-width: inherit;
}
.has__lists {
  display: flex;
}
.list {
  padding: 10rem;
  border: 1px solid #8a2be2;
  border-radius: 2rem;
  margin-left: 2rem;
  margin-top: 5rem;
  padding-bottom: 0px;
  width: 20%;
}
.title {
  background: #8a2be2;
  color: white;
  width: 320px;
  text-align: center;
  margin-left: -10rem;
  margin-top: -10rem;
  height: 100px;
  border-top-left-radius: 2rem;
  border-top-right-radius: 2rem;
}
.footer {
  margin-top: 10rem;
  background: white;
  color: black;
  width: 320px;
  margin-left: -10rem;
  margin-top: 0.01rem;
  margin-bottom: 0rem;
  height: 100px;
  border-bottom-left-radius: 2rem;
  border-bottom-right-radius: 2rem;
  text-align: center;
}
.body {
  background-color: white;
  width: 320px;
  color: black;
  margin-left: -10rem;
  text-align: center;
  min-height: 10rem;
  height: fit-content;
}
.list_name {
  margin-top: 0.6rem;
  padding: 2px;
  font-weight: 600;
  font-size: 20px;
  border-top-left-radius: 1rem;
  border-bottom-left-radius: 1rem;
}
.list__icon {
  width: 20px;
  height: 20px;
}
.title__options {
  display: flex;
  justify-content: center;
}
.list_plus {
  padding: 0.4rem;
  border: 1px solid gray;
  border-radius: 1rem;
  transition: var(--transition);
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
.list_plus:hover {
  background: black;
  color: #8a2be2;
  border: 1px solid white;
}
.task__ui {
  border: 1px solid grey;
  border-width: 80%;
  width: 75%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 0.2rem;
  border-radius: 1rem;
}
.deadline {
  font-weight: 800;
  color: black;
}

.task_title_options {
  display: flex;
}
.task__title {
  align-self: center;
  margin-left: auto;
  margin-right: auto;
}
.task__dropdown {
  margin-top: -0.5rem;
  margin-right: 1rem;
}
.exportbtn {
  margin-top: 1.2rem;
  color: #8a2be2;
  border: 1px solid #8a2be2;
}
.export_task {
  text-decoration: none;
}
.dropdown_m {
  width: 80%;
  height: 60%;
  margin-left: 1.5rem;
  margin-bottom: 0.5rem;
  margin-top: 0.5rem;
}
</style>
