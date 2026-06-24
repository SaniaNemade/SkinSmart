"""
Nuclear option: Extract model using TF1 compatibility or raw pb file parsing
"""
import tensorflow as tf
import os
import sys

def extract_with_tf1_compat(savedmodel_path, output_path):
    """
    Use TF1 compatibility to load the model
    """
    print(f"Attempting TF1 compatibility mode for {savedmodel_path}...")
    
    try:
        # Disable eager execution temporarily
        tf.compat.v1.disable_eager_execution()
        
        # Create a new graph
        with tf.compat.v1.Session(graph=tf.compat.v1.Graph()) as sess:
            # Load the SavedModel
            tf.compat.v1.saved_model.loader.load(
                sess,
                [tf.compat.v1.saved_model.tag_constants.SERVING],
                savedmodel_path
            )
            
            # Get the graph
            graph = tf.compat.v1.get_default_graph()
            
            # Find input and output tensors
            # Common input names
            possible_inputs = ['input_1:0', 'input:0', 'x:0', 'inputs:0']
            input_tensor = None
            for inp in possible_inputs:
                try:
                    input_tensor = graph.get_tensor_by_name(inp)
                    print(f"Found input tensor: {inp}")
                    break
                except:
                    continue
            
            if input_tensor is None:
                # List all operations to find input
                print("Available operations:")
                for op in graph.get_operations()[:20]:
                    print(f"  {op.name}: {op.type}")
                return False
            
            # Find output tensor
            possible_outputs = ['dense/Softmax:0', 'predictions:0', 'output:0', 'Identity:0']
            output_tensor = None
            for out in possible_outputs:
                try:
                    output_tensor = graph.get_tensor_by_name(out)
                    print(f"Found output tensor: {out}")
                    break
                except:
                    continue
            
            if output_tensor is None:
                # List last operations
                print("Last 20 operations:")
                ops = graph.get_operations()
                for op in ops[-20:]:
                    print(f"  {op.name}: {op.type}")
                return False
            
            print(f"Input shape: {input_tensor.shape}")
            print(f"Output shape: {output_tensor.shape}")
        
        # Re-enable eager execution
        tf.compat.v1.enable_eager_execution()
        
        # Now load normally but use concrete function
        loaded = tf.saved_model.load(savedmodel_path)
        concrete_func = loaded.signatures['serving_default']
        
        # Create Keras model from concrete function
        input_spec = concrete_func.structured_input_signature[1]
        input_name = list(input_spec.keys())[0]
        input_shape = input_spec[input_name].shape.as_list()
        
        @tf.function
        def model_fn(x):
            return concrete_func(**{input_name: x})
        
        # Wrap in Keras
        inputs = tf.keras.Input(shape=input_shape[1:])
        outputs = tf.keras.layers.Lambda(lambda x: list(model_fn(x).values())[0])(inputs)
        model = tf.keras.Model(inputs, outputs)
        
        # Save
        model.save(output_path)
        print(f"✓ Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ TF1 compat failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Ensure eager execution is restored
        if not tf.executing_eagerly():
            tf.compat.v1.enable_eager_execution()

def simple_wrapper_approach(savedmodel_path, output_path):
    """
    Simplest possible approach - just wrap the signature
    """
    print(f"\nTrying simple wrapper for {savedmodel_path}...")
    
    try:
        # Load just the inference function - don't touch the optimizer
        loaded = tf.saved_model.load(savedmodel_path, tags=['serve'])
        
        # Get inference function
        infer = loaded.signatures['serving_default']
        
        # Get specs
        input_spec = infer.structured_input_signature[1]
        input_name = list(input_spec.keys())[0]
        input_shape = [None, 224, 224, 3]  # Standard image input
        
        print(f"Using input shape: {input_shape}")
        
        # Create wrapper model
        class WrapperModel(tf.keras.Model):
            def __init__(self, infer_fn, input_name):
                super().__init__()
                self.infer_fn = infer_fn
                self.input_name = input_name
                
            def call(self, inputs, training=False):
                result = self.infer_fn(**{self.input_name: inputs})
                output_key = list(result.keys())[0]
                return result[output_key]
        
        model = WrapperModel(infer, input_name)
        
        # Build the model
        model.build((None, 224, 224, 3))
        
        # Test it
        import numpy as np
        test_input = np.random.random((1, 224, 224, 3)).astype(np.float32)
        test_output = model(test_input)
        print(f"Test output shape: {test_output.shape}")
        
        # Save
        model.save(output_path)
        print(f"✓ Saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Simple wrapper failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    models = [
        ('./models/skin_model', './models/skin_model.keras'),
        ('./models/acne_model', './models/acne_model.keras')
    ]
    
    for savedmodel_path, output_path in models:
        print("\n" + "=" * 70)
        print(f"PROCESSING: {os.path.basename(savedmodel_path)}")
        print("=" * 70)
        
        # Try simple wrapper first
        success = simple_wrapper_approach(savedmodel_path, output_path)
        
        if not success:
            # Try TF1 compat as last resort
            success = extract_with_tf1_compat(savedmodel_path, output_path)
        
        if success:
            print(f"\n✓✓✓ {os.path.basename(savedmodel_path)} converted successfully!")
        else:
            print(f"\n✗✗✗ Failed to convert {os.path.basename(savedmodel_path)}")

if __name__ == "__main__":
    main()