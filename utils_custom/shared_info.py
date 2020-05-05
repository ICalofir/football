from absl import logging

class SharedInfo():
    def save_info(self, info, step):
        if step % 100 == 0:
            logging.info('Save info for frames at step: {}'.format(step))
