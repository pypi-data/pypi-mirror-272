#include "internal.h"

struct CommandList* command_list_create_extern(struct Context* context) {
    LOG_INFO("Creating command list with context %p", context);

    struct CommandList* command_list = new struct CommandList();
    command_list->ctx = context;
    return command_list;
}

void command_list_destroy_extern(struct CommandList* command_list) {
    for(int i = 0; i < command_list->stages.size(); i++) {
        free(command_list->stages[i].user_data);
    }

    delete command_list;
}

void command_list_get_instance_size_extern(struct CommandList* command_list, unsigned long long* instance_size) {
    size_t instance_data_size = 0;

    for(int i = 0; i < command_list->stages.size(); i++) {
        instance_data_size += command_list->stages[i].instance_data_size;
    }

    *instance_size = instance_data_size;

    LOG_INFO("Instance size: %llu", *instance_size);
}

void command_list_reset_extern(struct CommandList* command_list) {
    LOG_INFO("Resetting command list");

    for(int i = 0; i < command_list->stages.size(); i++) {
        free(command_list->stages[i].user_data);
    }

    command_list->stages.clear();
}

void command_list_submit_extern(struct CommandList* command_list, void* instance_buffer, unsigned int instance_count, int* devices, int device_count, int* submission_thread_counts) {
    // For now, we will just submit the command list to the first device
    int device = devices[0];

    LOG_INFO("Submitting command list to device %d", device);

    char* instance_data = (char*)instance_buffer;
    char* current_instance_data = instance_data;

    //command_list->ctx->commandBuffers[device]->reset();

    VkFence waitFence = command_list->ctx->commandBuffers[device]->fence();

    command_list->ctx->commandBuffers[device]->begin();

    VkMemoryBarrier memory_barrier = {
            VK_STRUCTURE_TYPE_MEMORY_BARRIER,
            0,
            VK_ACCESS_SHADER_WRITE_BIT,
            VK_ACCESS_SHADER_READ_BIT,
    };

    for(size_t instance = 0; instance < instance_count; instance++) {
        LOG_INFO("Recording instance %d", instance);

        current_instance_data = instance_data;

        for (size_t i = 0; i < command_list->stages.size(); i++) {
            LOG_INFO("Recording stage %d", i);
            command_list->stages[i].record(command_list->ctx->commandBuffers[device], &command_list->stages[i], current_instance_data, device);
            if(i < command_list->stages.size() - 1)
                vkCmdPipelineBarrier(
                    command_list->ctx->commandBuffers[device]->handle(), 
                    command_list->stages[i].stage, 
                    command_list->stages[i+1].stage, 
                    0, 1, 
                    &memory_barrier, 
                    0, 0, 0, 0);
            current_instance_data += command_list->stages[i].instance_data_size;
        }
    }

    command_list->ctx->commandBuffers[device]->end();

    command_list->ctx->devices[device]->waitForFence(waitFence);

    command_list->ctx->queues[device]->submit(command_list->ctx->commandBuffers[device]);
    //command_list->ctx->queues[device]->waitIdle();
}