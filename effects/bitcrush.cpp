#include <stdio.h>
#include <stdint.h>

int main() {
    const int BITS = 8;          // ビット深度（4=超荒い、8=ファミコン風、16=原音）
    const int DOWNSAMPLE = 4;    // サンプルレート削減（1=なし、4=1/4に削減）
    const float VOLUME = 0.5f;

    const int levels = 1 << BITS;
    int16_t held_sample = 0;
    int counter = 0;

    int16_t sample;
    while (fread(&sample, sizeof(int16_t), 1, stdin) == 1) {
        // サンプルレート削減
        if (counter % DOWNSAMPLE == 0) {
            // ビット深度削減
            int32_t s = sample;
            s = (s / (65536 / levels)) * (65536 / levels);
            s = (int32_t)(s * VOLUME);
            if (s > 32767) s = 32767;
            if (s < -32768) s = -32768;
            held_sample = (int16_t)s;
        }
        counter++;
        fwrite(&held_sample, sizeof(int16_t), 1, stdout);
    }
    return 0;
}

