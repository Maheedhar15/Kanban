<template>
  <div class="Logout"></div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
export default {
  name: 'LogOut',
  data() {
    return {
      router: useRouter(),
    };
  },
  mounted() {
    const router = useRouter();
    const token = localStorage['access_token'];
    axios
      .delete('http://localhost:5000/logout', {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res);
        alert('You have been logged out');
        router.push({ name: 'Login' });
      })
      .catch((err) => {
        if (err.response.status == 401) {
          alert('Token UNAUTHORIZED');
          this.router.push({ name: 'Login' });
        }
        console.log(err);
      });
  },
};
</script>

<style></style>
