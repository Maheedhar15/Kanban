<template>
  <div class="dropdown">
    <button @click="toggleMenu">
      <fa class="dropdown_icon" icon="fa-solid fa-arrow-down" />
    </button>
    <div v-if="showMenu" class="menu">
      <div class="menu-item" @click="itemClicked">
        <router-link :to="`/updateList/${id}`" class="list__link"
          >Update</router-link
        >
        <br />
        <router-link :to="`/deleteList/${id}`" class="list__link"
          >Delete</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropdownList',
  props: ['id'],
  data() {
    return {
      showMenu: false,
    };
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    itemClicked() {
      this.toggleMenu();
    },
  },
};
</script>

<style scoped>
.dropdown_icon {
  padding: 0.2rem;
  color: white;
  background: black;
  margin-top: 15px;
  transition: var(--transition);
  border-radius: 0.2rem;
  height: 17px;
}
.dropdown_icon:hover {
  background: white;
  color: black;
  height: 17px;
}
.menu {
  background: white;
  padding-left: 2rem;
  padding-right: 2rem;
  border-radius: 1rem;
}
.list_plus {
  padding: 0.5rem;
  border: 1px solid gray;
  border-radius: 1rem;
  transition: var(--transition);
}
.list_plus:hover {
  background: black;
  color: #ffd700;
}
.createList {
  text-decoration: none;
}

.list__link {
  text-decoration: none;
  color: black;
  transition: var(--transition);
}
.list__link:hover {
  background: black;
  color: white;
  padding: 0.4rem;
  border-radius: 0.5rem;
}
</style>
