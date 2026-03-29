<template>
    <div class="notification_container">
        <div class="notification_holder">
            <p class="notification">{{ message }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        props:["message"],
    }
</script>