# # https://github.com/apple/ml-cvnets/blob/84d992f413e52c0468f86d23196efd9dad885e6f/cvnets/modules/mobilevit_blockops.py#L186
# def unfolding(self, feature_map):
#     """
#     ### Notations (wrt paper) ###
#         B/b = batch
#         P/p = patch_size
#         N/n = number of patches
#         D/d = embedding_dim

#     H, W
#     [                            [
#         [1, 2, 3, 4],     Goal      [1, 3, 9, 11],
#         [5, 6, 7, 8],     ====>     [2, 4, 10, 12],
#         [9, 10, 11, 12],            [5, 7, 13, 15],
#         [13, 14, 15, 16],           [6, 8, 14, 16]
#     ]                            ]
#     """

#     # Initially convert channel-last to channel-first for processing
#     shape = kops.shape(feature_map)
#     batch_size, orig_h, orig_w, in_channels = shape[0], shape[1], shape[2], shape[3]
#     feature_map = kops.transpose(feature_map, [0, 3, 1, 2])  # [B, H, W, C] -> [B, C, H, W]

#     patch_area = self.patch_size_w * self.patch_size_h

#     orig_h, orig_w = kops.cast(orig_h, dtype="int32"), kops.cast(orig_w, dtype="int32")

#     h_ceil = kops.ceil(orig_h / self.patch_size_h)
#     w_ceil = kops.ceil(orig_w / self.patch_size_w)

#     new_h = kops.cast(h_ceil * kops.cast(self.patch_size_h, dtype=h_ceil.dtype), dtype="int32")
#     new_w = kops.cast(w_ceil * kops.cast(self.patch_size_w, dtype=h_ceil.dtype), dtype="int32")

#     # Condition to decide if resizing is necessary
#     resize_required = kops.logical_or(kops.not_equal(new_w, orig_w), kops.not_equal(new_h, orig_h))
#     feature_map = kops.cond(
#         resize_required,
#         true_fn=lambda: kops.image.resize(feature_map, [new_h, new_w], data_format="channels_first"),
#         false_fn=lambda: feature_map,
#     )

#     num_patch_h = new_h // self.patch_size_h
#     num_patch_w = new_w // self.patch_size_w
#     num_patches = num_patch_h * num_patch_w

#     # Handle dynamic shape multiplication
#     dynamic_shape_mul = kops.prod([batch_size, in_channels * num_patch_h])

#     # Reshape and transpose to create patches
#     # [B, D, H, W] -> [B * D * n_h, p_h, n_w, p_w]
#     reshaped_fm = kops.reshape(feature_map, [dynamic_shape_mul, self.patch_size_h, num_patch_w, self.patch_size_w])

#     # [B * D * n_h, p_h, n_w, p_w] -> [B * D * n_h, n_w, p_h, p_w]
#     transposed_fm = kops.transpose(reshaped_fm, [0, 2, 1, 3])

#     # [B * D * n_h, n_w, p_h, p_w] -> [B, D, N, P] where P = p_h * p_w and N = n_h * n_w
#     reshaped_fm = kops.reshape(transposed_fm, [batch_size, in_channels, num_patches, patch_area])

#     # [B, D, N, P] -> [B, P, N, D]
#     transposed_fm = kops.transpose(reshaped_fm, [0, 3, 2, 1])

#     # [B, P, N, D] -> [BP, N, D]
#     patches = kops.reshape(transposed_fm, [batch_size * patch_area, num_patches, in_channels])

#     info_dict = {
#         "orig_size": (orig_h, orig_w),
#         "batch_size": batch_size,
#         "interpolate": resize_required,
#         "total_patches": num_patches,
#         "num_patches_w": num_patch_w,
#         "num_patches_h": num_patch_h,
#         "patch_area": patch_area,
#     }

#     return patches, info_dict

# https://github.com/apple/ml-cvnets/blob/84d992f413e52c0468f86d23196efd9dad885e6f/cvnets/modules/mobilevit_block.py#L233
# def folding(self, patches, info_dict, outH, outW, outC):
#     # Ensure the input patches tensor has the correct dimensions
#     assert len(patches.shape) == 3, f"Tensor should be of shape BPxNxD. Got: {patches.shape}"

#     # Reshape to [B, P, N, D]
#     patches = kops.reshape(patches, [info_dict["batch_size"], info_dict["patch_area"], info_dict["total_patches"], -1])

#     # Get shape parameters for further processing
#     shape = kops.shape(patches)
#     batch_size = shape[0]
#     channels = shape[3]

#     num_patch_h = info_dict["num_patches_h"]
#     num_patch_w = info_dict["num_patches_w"]

#     # Transpose dimensions [B, P, N, D] --> [B, D, N, P]
#     patches = kops.transpose(patches, [0, 3, 2, 1])

#     # Calculate total elements dynamically
#     num_total_elements = batch_size * channels * num_patch_h

#     # Reshape to match the size of the feature map before splitting into patches
#     # [B, C, N, P] --> [B*C*n_h, n_w, p_h, p_w]
#     feature_map = kops.reshape(patches, [num_total_elements, num_patch_w, self.patch_size_h, self.patch_size_w])

#     # Transpose to switch width and height axes [B*C*n_h, n_w, p_h, p_w] --> [B*C*n_h, p_h, n_w, p_w]
#     feature_map = kops.transpose(feature_map, [0, 2, 1, 3])

#     # Reshape back to the original image dimensions [B*C*n_h, p_h, n_w, p_w] --> [B, C, H, W]
#     # Reshape back to [B, C, H, W]
#     new_height = num_patch_h * self.patch_size_h
#     new_width = num_patch_w * self.patch_size_w
#     feature_map = kops.reshape(feature_map, [batch_size, -1, new_height, new_width])

#     # # Conditional resizing using kops.cond
#     # feature_map = kops.cond(
#     #     info_dict["interpolate"],
#     #     lambda: kops.image.resize(feature_map, info_dict["orig_size"], data_format="channels_first"),
#     #     lambda: feature_map,
#     # )

#     feature_map = kops.transpose(feature_map, [0, 2, 3, 1])
#     feature_map = kops.reshape(feature_map, (batch_size, outH, outW, outC))

# return feature_map


# def call(self, x):

#     fmH, fmW = kops.shape(x)[1], kops.shape(x)[2]

#     local_representation = self.local_rep_layer_1(x)
#     local_representation = self.local_rep_layer_2(local_representation)
#     out_channels = local_representation.shape[-1]

#     # Transformer as Convolution Steps
#     # --------------------------------
#     # # Unfolding

#     unfolded, info_dict = self.unfolding(local_representation)

#     # # Infomation sharing/mixing --> global representation
#     for layer in self.transformer_layers:
#         unfolded = layer(unfolded)

#     global_representation = self.transformer_layer_norm(unfolded)

#     # #Folding
#     folded = self.folding(
#         global_representation,
#         info_dict=info_dict,
#         # outH=fmH,
#         # outW=fmW,
#         # outC=out_channels,
#     )

#     # Fusion
#     local_mix = self.local_features_3(folded)
#     fusion = self.concat([x, local_mix])
#     fusion = self.fuse_local_global(fusion)

#     return fusion
