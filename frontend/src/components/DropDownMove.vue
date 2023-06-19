<template>
  <div class="dropdown">
    <v-btn @click="toggleMenu" elevation="2" outlined>Move</v-btn>
    <div v-if="showMenu" class="menu">
      <div
        class="menu-item"
        @click="itemClicked"
        v-for="(item, index) in items"
        :key="index"
      >
        <router-link
          :to="`/moveTask/${tid}/${item.list_id}`"
          class="list__link"
          >{{ item.list_name }}</router-link
        >
        <br />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropdownList',
  props: ['tid', 'items'],
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
  color: grey;
  background: transparent;
  margin-top: 15px;
  transition: var(--transition);
  border: 1px solid black;
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
  color: white;
  background: black;
  border-radius: 0.5rem;
  padding: 0.4rem;
}
</style>
