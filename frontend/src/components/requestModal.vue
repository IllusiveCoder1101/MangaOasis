<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Request</h1>
                <button @click="close_func(true,true,true,true,true)" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container">
                        <label for="card_name" class="modal_label">Hrs</label>
                        <input type="number" name="" id="" @input="handle_input1($event.target.value)" class="modal_input" placeholder="00" required>
                    </div>
                    <div class="detail_container">
                        <label for="card_name" class="modal_label">mins</label>
                        <input type="number" name="" id="" @input="handle_input2($event.target.value)" class="modal_input" placeholder="00" required>
                    </div>
                    <div class="detail_container">
                        <label for="card_name" class="modal_label">sec</label>
                        <input type="number" name="" id="" @input="handle_input3($event.target.value)" class="modal_input" placeholder="00" required>
                        
                    </div>
                </div>
                <p v-if="error_msg" class="error_msg">{{ error_msg }}</p>
                <button type="submit" :disabled="(error_msg==='Invalid Time')?true:false" class="primary_btn1" @click.prevent="()=>{handle_submit(hrs,mins,sec)}">Place Your Request</button>
         
            </form>
        </div>
    </section>
</template>

<script>
    import { ref } from 'vue'
    export default{
        data(){
            return {
                hrs:ref({"value":''}),
                mins:ref({"value":''}),
                sec:ref({"value":''}),
                error_msg:''
            }
        },
        methods:{
            handle_input1(input){
                if(parseInt(input)>=0){
                    this.hrs.value=parseInt(input)
                }
                else{
                    this.error_msg='Invalid Time'
                }
            },
            handle_input2(input){
                if(parseInt(input)>=0){
                    this.mins.value=parseInt(input)
                }
                else{
                    this.error_msg='Invalid Time'
                }
            },
            handle_input3(input){
                if(parseInt(input)>=0){
                    this.sec.value=parseInt(input)
                }
                else{
                    this.error_msg='Invalid Time'
                }
            },
            

        },
        props:["close_func",'handle_submit']
    }
</script>