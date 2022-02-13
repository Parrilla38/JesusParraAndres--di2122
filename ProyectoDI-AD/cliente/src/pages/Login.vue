<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 400px">
      <q-form class="q-gutter-md">
        <q-input
          filled
          v-model="name"
          label="Usuari"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Escriu algo']"
        >
          <q-avatar>
            <img src="./../../public/icons/favicon-128x128.png" />
          </q-avatar>
        </q-input>

        <q-input
          filled
          type="password"
          v-model="password"
          label="Password"
          lazy-rules
          :rules="[ valor => valor !== null && valor !== '' || 'Escriu la contrasenya']"
        >
          <q-icon name="password" />
        </q-input>

        <div>
          <q-btn label="Login" class="full-width" size="lg" type="submit" color="primary" />
          <!--
            afegim baix del boto de login el boto del drawer
          -->
           <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            @click="drawerState=!drawerState"/>
        </div>
        <q-card-section class="text-center q-pa-none">
          <p class="text-grey-6">
            No estas registrat?
            <a href="#/Register">Registrat</a>
          </p>
        </q-card-section>
      </q-form>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Pagina Login',
  data () {
    return {
      name: '',
      password: ''
    }
  },
  computed: {
    drawerState: {
      get () {
        return this.$store.state.showcase.drawerState
      },
      set (val) {
        this.$store.commit('showcase/updateDrawerState', val)
      }
    }
  }
}
</script>