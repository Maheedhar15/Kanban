<template>
  <div class="navbar">
    <nav class="navbar__bar">
      <router-link :to="`/dashboard/${id}`" class="nav-item">
        <h3 class="nav-item app__name">Kanban</h3></router-link
      >
      <a :href="`http://localhost:5000/export/${id}`" class="nav-item"
        ><h3 class="nav-item">Export</h3></a
      >

      <router-link :to="`/summary/${id}`" class="nav-item"
        ><h3 class="nav-item">Summary</h3>
      </router-link>
      <div class="text-center">
        <router-link :to="`/logout/${id}`" class="nav-item user__icon"
          ><h3>Logout</h3></router-link
        >
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  props: ['id'],
  data: () => ({}),
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik&display=swap');
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital@1&family=Rubik&display=swap');
.navbar__bar {
  font-family: 'Rubik';
  display: flex;
  gap: 1.5rem;
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
  padding-left: 0.5rem;
  border: 1px solid transparent;
}
.nav-item {
  font-weight: 900;
  font-size: 17px;
  text-decoration: none;
  color: white;
}
.app__name {
  font-family: 'IBM Plex Mono';
  font-style: italic;
}
.user__icon {
  margin-top: -1px;
  margin-left: 95rem;
  position: fixed;
}
.btn {
  background: transparent;
  border: transparent;
  width: 10%;
}
</style>
