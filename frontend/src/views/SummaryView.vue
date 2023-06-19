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
                <h1 class="list_name">{{ item.list_name }}</h1>
                <!-- V-menu -->
                <!--menu ends-->
              </div>
            </div>
            <div class="body">
              <h3>No of Tasks: {{ item.no_of_tasks }}</h3>
              <br />
              <p class="completed_task">
                No of Completed tasks: {{ item.no_completed }}
              </p>
              <br />
              <p class="crossed_deadline">
                No. of tasks that crossed deadline:
                {{ item.no_crossed_deadline }}
              </p>
              <br />
              <p>Analysis Chart:</p>
              <br />
              <Bar
                :id="`${item.list_id}`"
                :labels="`${item.labels}`"
                :values="`${item.no_of_tasks_list}`"
                :no_completed="`${item.no_completed_tasks_list}`"
                :no_crossed="`${item.no_of_deadline_crossed_tasks_list}`"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import Navbar from '../components/NavBar.vue';
import Bar from '../components/AnalysisBarChart.vue';
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
      labels: [],
    };
  },
  methods: {
    getSummary() {
      const path = 'http://localhost:5000/summary/' + this.$route.params.id;
      const token = localStorage['access_token'];
      axios
        .get(path, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.items = res.data.list;
          this.availableLists = res.data.availableLists;
          this.len_list = res.data.list[0]['len_list'];
          console.log(res.data.list[0]['no_completed_tasks_list']);
        })

        .catch((err) => {
          console.log(err);
        });

      console.log(this.items);
    },
  },
  components: {
    Navbar,

    Bar,
  },
  created() {
    this.getSummary();
  },
};
</script>

<style scoped>
.dashboard {
  width: 100%;
  min-height: 100vh;
  color: #8a2be2;
  background-image: url('../assets/black-purple.jpg');
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
  background: #ffd700;
  color: black;
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
  border: 1px solid #ffd700;
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

.body {
  background-color: white;
  width: 320px;
  color: black;
  margin-left: -10rem;
  text-align: center;
  min-height: 10rem;
  height: fit-content;
  border-bottom-right-radius: 1rem;
  border-bottom-left-radius: 1rem;
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
  color: #ffd700;
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
.completed_task {
  color: green;
}
.crossed_deadline {
  color: red;
}
</style>
