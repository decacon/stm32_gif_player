#include "gif_player.h"

void GIF_Player_Init(GIF_Player *player, const uint16_t *frames, const uint16_t *delays,
                     uint32_t frame_count, uint16_t width, uint16_t height) {
    player->frames = (const uint16_t**)frames;
    player->delays = delays;
    player->frame_count = frame_count;
    player->width = width;
    player->height = height;
    player->current_frame = 0;
    player->last_frame_time = 0;
    player->default_delay_ms = 100;
    player->is_playing = 1;
}

void GIF_Player_Start(GIF_Player *player) {
    player->is_playing = 1;
}

void GIF_Player_Stop(GIF_Player *player) {
    player->is_playing = 0;
}

void GIF_Player_Restart(GIF_Player *player) {
    player->current_frame = 0;
    player->last_frame_time = HAL_GetTick();
    player->is_playing = 1;
}

void GIF_Player_SetSpeed(GIF_Player *player, uint16_t delay_ms) {
    player->default_delay_ms = delay_ms;
}

void GIF_Player_Update(GIF_Player *player) {
    if (!player->is_playing) return;

    uint32_t current_time = HAL_GetTick();

    // Default delay
    uint16_t current_delay = (player->delays != NULL) ?
                            player->delays[player->current_frame] :
                            player->default_delay_ms;

    if (current_time - player->last_frame_time >= current_delay) {
        // Changing next frame
        player->current_frame = (player->current_frame + 1) % player->frame_count;

        // Pointer for current frame
        const uint16_t *current_frame_data = player->frames[player->current_frame];

        // Display output
        ST7735_DrawImage(0, 0, player->width, player->height, current_frame_data);

        player->last_frame_time = current_time;
    }
}
