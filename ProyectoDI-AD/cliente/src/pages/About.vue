<template>
  <q-page class="flex flex-center" padding>
    <div class="full-width" style="max-width: 250px">
      <h5 class="q-my-sm text-center text-primary">ABOUT</h5>
      <q-card>
        <q-card-section>
          <div>
            <br>
            <b>
            Autor : {{autor}}
            </b>
            <br>
            Correo : {{correo}}
            <br>
            Curso : {{curso}}
            <br>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>


<script>
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'About',
  data () {
    return {
      autor: 'Jesús Parra',
      correo: 'parrilla38g@gmail.com',
      curso: '2n DAM'
    }
  }
})
</script>