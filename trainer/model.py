#!/usr/bin/python
def build_model_fn(self):
    def _model_fn(features, labels, mode, params):
        """Creates the prediction and its loss.

        Args:
          features: A dictionary of tensors keyed by the feature name.
          labels: A tensor representing the labels.
          mode: The execution mode, defined in tf.contrib.learn.ModeKeys.

        Returns:
          A tuple consisting of the prediction, loss, and train_op.
        """
        predictions = self.inference(features)
        if mode == tf.contrib.learn.ModeKeys.INFER:
            return predictions, None, None

        loss = self.loss(predictions, labels)
        if mode == tf.contrib.learn.ModeKeys.EVAL:
            return predictions, loss, None

        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            learning_rate=params["learning_rate"],
            optimizer='Adagrad',
            summaries=[
                "learning_rate",
                "loss",
                "gradients",
                "gradient_norm",
            ],
            name='train')

        else:
            return predictions, loss, train_op

    return _model_fn