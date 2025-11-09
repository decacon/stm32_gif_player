/*
 * gif_player.h
 *
 *  Created on: Nov 6, 2025
 *      Author: Decadance
 */

#ifndef GIF_PLAYER_GIF_PLAYER_H_
#define GIF_PLAYER_GIF_PLAYER_H_

#include "image_conf.h"
#include "main.h"
#include "st7735.h"

typedef struct {
    const uint16_t **frames;
    const uint16_t *delays;
    uint32_t frame_count;
    uint16_t width;
    uint16_t height;
    uint32_t current_frame;
    uint32_t last_frame_time;
    uint16_t default_delay_ms;
    uint8_t is_playing;
} GIF_Player;

// player init
void GIF_Player_Init(GIF_Player *player, const uint16_t *frames, const uint16_t *delays,
                     uint32_t frame_count, uint16_t width, uint16_t height);

// animation function
void GIF_Player_Update(GIF_Player *player);

// Playback control
void GIF_Player_Start(GIF_Player *player);
void GIF_Player_Stop(GIF_Player *player);
void GIF_Player_Restart(GIF_Player *player);

// Speed control
void GIF_Player_SetSpeed(GIF_Player *player, uint16_t delay_ms);


#endif /* GIF_PLAYER_GIF_PLAYER_H_ */
