<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Edit Chapter</h1>
                <button @click="close_func('')" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_name" class="modal_label">Volume</label>
                        <input type="number"  id="card_name" placeholder="10" class="modal_input" :value="chapter_data1['volume_no']" @input="chapter_data['volume_no']=$event.target.value">
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Chapter</label>
                        <input type="number"  id="expiry" placeholder="123" class="modal_input" :value="chapter_data1['chapter_no']" @input="chapter_data['chapter_no']=$event.target.value">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Chapter Title</label>
                        <input type="text"  id="expiry" placeholder="XYZ" class="modal_input" :value="chapter_data1['chapter_name']" @input="chapter_data['chapter_name']=$event.target.value">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Chapter Pages</label>
                        <input type="file" name="" id="" ref="file"  class="modal_input" multiple @change="chapter_data['chapter_pages']=read_img()">
                    </div>
                    
                </div>
                <div v-if="error.length>0" class="error_state3">
                    <p class="error_msg">{{ error }}</p>
                </div>
                <div class="payment_details">
                    
                    <button type="submit" class="primary_btn1" @click.prevent="handle_chapter_edit(chapter_data,chapter_data1['chapter_id'])">Edit Chapter</button>
                </div>
            </form>
        </div>
    </section>
</template>
<script setup>
    import { ref } from 'vue';

    const chapter_data=ref({"book_id":"","volume_no":"","chapter_no":"","chapter_name":"","chapter_pages":""})

</script>
<script>
    export default {
        props:["close_func","chapter_data1","handle_chapter_edit","error"],
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