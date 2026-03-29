<template>
    <section class="modal">
        <div class="modal_container">      
            <header class="modal_head">
                <h1 class="modal_header">Add Chapter</h1>
                <button @click="close_func()" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_name" class="modal_label">Volume</label>
                        <input type="number"  id="card_name" placeholder="10" class="modal_input" v-model="chapter_data['volume_no']" required>
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Chapter</label>
                        <input type="number"  id="expiry" placeholder="123" class="modal_input" v-model="chapter_data['chapter_no']" required>
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Chapter Title</label>
                        <input type="text"  id="expiry" placeholder="XYZ" class="modal_input"  v-model="chapter_data['chapter_name']" required>
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Chapter Pages</label>
                        <input type="file" name="" id="" ref="file"  class="modal_input" multiple @change="chapter_data['chapter_pages']=read_img()" required>
                    </div>
                    
                </div>
                <div v-if="error.length>0" class="error_state3">
                    <p class="error_msg">{{ error }}</p>
                </div>
                <div class="payment_details">  
                    <button type="submit" class="primary_btn1" :disabled="checkData()" @click.prevent="handle_add_chapter({'book_id':book_id,...chapter_data})">Add Chapter</button>
                </div>
            </form>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue';

    const chapter_data=ref({"volume_no":"","chapter_no":"","chapter_name":"","chapter_pages":""})
    const checkData=()=>{
                
        if (chapter_data.value['volume_no'] && chapter_data.value["chapter_no"] && chapter_data.value["chapter_name"] && chapter_data.value["chapter_pages"] ) {
                   
            return false
        }
        else{
                    
            return true
        }
    }
</script>

<script>
    export default {
        props:["close_func","handle_add_chapter","book_id","error"],
        methods:{
            
            read_img(){
                let l=[]
            
                for (let i of this.$refs.file.files){
                    l.push(i.name)
                }
                
                return l.join()
            }
        }
    }
</script>