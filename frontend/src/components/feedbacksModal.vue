<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Feedbacks</h1>
                <button @click="close_func(0)" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <div class="issue_book_container">
                <div v-if="user_feedbacks.length>0">
                    <div class="issue_profile2" v-for="i in user_feedbacks" :key="i">
                        <div class="issue_desc1">
                            <div class="issue_text1">
                                <img :src="getBookCover(i['book_id'])" alt="profile_pic" class="profile_pic">
                                <div class="user_card_desc">
                                    <p class="user_card_name1">{{ getBookById(i["book_id"])[0]["book_name"] || "" }}</p>
                                    <p class="user_card_email1">{{ getBookById(i["book_id"])[0]["author_name"] || "" }}</p>
                                </div>
                            </div>
                            <h2 class="score">{{ i["feedback_score"] }}<em>/ 10</em></h2>
                        </div>
                        <p class="desc2">{{ i["feedback_message"]  }}</p>
                    </div>
                </div>
                <div v-else class="error_state1">
                        <p class="error_msg1">No Feedbacks Provided</p>
                </div>
            </div>
            
        </div>
    </section>
</template>

<script>
    export default {
        props:["close_func","user_feedbacks","getBookById","getBookCover"]
    }
</script>