<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 400px">

    <q-form
      class="q-gutter-md" @submit="validateForm" action="/" method="post"
    >
      <q-input
        filled
        v-model="nom_comp"
        label="Nombre Completo"
        lazy-rules
        :rules="[ val => nombre_valido || 'Introduce un nombre válido!']"
      >
        <q-icon name="text_format"/>
      </q-input>

      <q-input
        filled
        v-model="dni"
        label="DNI"
        lazy-rules
        :rules="[ val => valid_DNI || 'Introduce el DNI válido!']"
       >
        <q-icon name="credit_card"/>
      </q-input>
      <q-input
        filled
        v-model="nom"
        label="Usuario"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Introduce un nombre de usuario válido!']"
      >
        <q-icon name="perm_identity"/>
      </q-input>
      <q-input
        filled
        type="password"
        v-model="contra"
        label="Contraseña"
        lazy-rules
        :rules="[ val => val.length >= 4 || 'Introduce una contraseña!']"
      >
        <q-icon name="password"/>
      </q-input>
      <q-input
        filled
        type="password"
        v-model="contra2"
        label="Repite la Contraseña"
        lazy-rules
        :rules="[ val => val === this.password || 'Las contraseñas no coinciden!']"
      >
        <q-icon name="password"/>
      </q-input>
      <div>
        <q-btn label="Registrar" class="full-width" size="lg" type="submit" color="primary"/>
      </div>
    </q-form>

  </div>
  </q-page>
</template>
<script>
export default {
  name: 'Register',
  data () {
    return {
      nom_comp: '',
      dni: '',
      nom: '',
      contra: '',
      contra2: ''
    }
  },
  computed: {
    valid_DNI () {
      const dni_validar = /[0-9]{8}[A-Za-z]/
      return dni_validar.test(this.dni)
    },
    nombre_valido () {
        const noms = this.nom_comp.split(' ')
        if (noms[0].length > 3 && noms[1].length > 3) {
            return true
        } else {
            return false
        }
    }
  }
}
</script>