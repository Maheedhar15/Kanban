import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import DashboardView from '../views/DashboardView.vue';
import CreateList from '../views/CreateList.vue';
import CreateTask from '../views/CreateTask.vue';
import updateList from '../views/updateList.vue';
import deleteList from '../views/DeleteList.vue';
import updateTask from '../views/updateTask.vue';
import DeleteTask from '../views/DeleteTask.vue';
import LogOut from '../views/LogOut.vue';
import SummaryView from '../views/SummaryView.vue';
import MoveTask from '../views/MoveTask.vue';
import ForgotPass from '../views/ForgotPass.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/dashboard/:id',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/createList/:id',
    name: 'CreateList',
    component: CreateList,
  },
  {
    path: '/createTask/:uid/:lid',
    name: 'CreateTask',
    component: CreateTask,
  },
  {
    path: '/updateList/:lid',
    name: 'updateList',
    component: updateList,
  },
  {
    path: '/deleteList/:lid',
    name: 'deleteList',
    component: deleteList,
  },
  {
    path: '/updateTask/:tid',
    name: 'updateTask',
    component: updateTask,
  },
  {
    path: '/deleteTask/:tid',
    name: 'deleteTask',
    component: DeleteTask,
  },
  {
    path: '/logout/:id',
    name: 'Logout',
    component: LogOut,
  },
  {
    path: '/summary/:id',
    name: 'Summary',
    component: SummaryView,
  },
  {
    path: '/moveTask/:tid/:lid',
    name: 'MoveTask',
    component: MoveTask,
  },
  {
    path: '/forgotpassword',
    name: 'Forgot Password',
    component: ForgotPass,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
