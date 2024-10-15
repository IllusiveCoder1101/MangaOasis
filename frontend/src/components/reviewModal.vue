<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Review</h1>
                <button @click="close_func()" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="review_details">
                    <div class="detail_container4">
                        <label for="score" class="modal_label">Score</label>
                        <input type="number" v-model="score.value" id="score" placeholder="0" class="modal_input3" required>
                    </div>
                    <div class="detail_container4">
                        <label for="comment" class="modal_label">Comment</label>
                        <textarea  id="comment" v-model="msg.value" cols="60" rows="7" class="modal_input2" placeholder="Write Your Views" required></textarea>
                    </div>
                </div>
                <button type="submit" :disabled="checkData()" class="primary_btn1" @click.prevent="()=>handle_submit(msg.value,score.value)">Submit Review</button>
                
            </form>
        </div>
    </section>
</template>

<script>
import { ref } from 'vue';

    export default{
        data(){
            return {
                msg:ref({"value":""}),
                score:ref({"value":""})
            }
        },
        props:["close_func","handle_submit"],
        methods:{
            checkData(){
                if (this.msg.value && this.score.value){
                    return false
                }
                else{
                    return true
                }
            }
        }
    }
</script>