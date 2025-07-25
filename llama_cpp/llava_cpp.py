from __future__ import annotations

import os
from ctypes import (
    c_bool,
    c_char_p,
    c_int,
    c_uint8,
    c_float,
    c_size_t,
    c_void_p,
    POINTER,
    _Pointer,  # type: ignore
    Structure,
)
import pathlib
from typing import (
    Union,
    NewType,
    Optional,
    TYPE_CHECKING,
)

import llama_cpp.llama_cpp as llama_cpp

from llama_cpp._ctypes_extensions import (
    load_shared_library,
    ctypes_function_for_shared_library,
)

if TYPE_CHECKING:
    from llama_cpp._ctypes_extensions import (
        CtypesArray,
    )


# Specify the base name of the shared library to load
_libllava_base_name = "llava"
_libllava_override_path = os.environ.get("LLAVA_CPP_LIB")
_libllava_base_path = pathlib.Path(os.path.abspath(os.path.dirname(__file__))) / "lib" if _libllava_override_path is None else pathlib.Path()

# Load the library
_libllava = load_shared_library(_libllava_base_name, _libllava_base_path)

ctypes_function = ctypes_function_for_shared_library(_libllava)


################################################
# llava.h
################################################

# struct clip_ctx;
clip_ctx_p = NewType("clip_ctx_p", int)
clip_ctx_p_ctypes = c_void_p


# struct llava_image_embed {
#     float * embed;
#     int n_image_pos;
# };
class llava_image_embed(Structure):
    _fields_ = [
        ("embed", POINTER(c_float)),
        ("n_image_pos", c_int),
    ]


# /** sanity check for clip <-> llava embed size match */
# LLAVA_API bool llava_validate_embed_size(const llama_context * ctx_llama, const clip_ctx * ctx_clip);
@ctypes_function(
    "llava_validate_embed_size",
    [llama_cpp.llama_context_p_ctypes, clip_ctx_p_ctypes],
    c_bool,
)
def llava_validate_embed_size(
    ctx_llama: llama_cpp.llama_context_p, ctx_clip: clip_ctx_p, /
) -> bool:
    ...


# /** build an image embed from image file bytes */
# LLAVA_API struct llava_image_embed * llava_image_embed_make_with_bytes(struct clip_ctx * ctx_clip, int n_threads, const unsigned char * image_bytes, int image_bytes_length);
@ctypes_function(
    "llava_image_embed_make_with_bytes",
    [clip_ctx_p_ctypes, c_int, POINTER(c_uint8), c_int],
    POINTER(llava_image_embed),
)
def llava_image_embed_make_with_bytes(
    ctx_clip: clip_ctx_p,
    n_threads: Union[c_int, int],
    image_bytes: CtypesArray[c_uint8],
    image_bytes_length: Union[c_int, int],
    /,
) -> "_Pointer[llava_image_embed]":
    ...


# /** build an image embed from a path to an image filename */
# LLAVA_API struct llava_image_embed * llava_image_embed_make_with_filename(struct clip_ctx * ctx_clip, int n_threads, const char * image_path);
@ctypes_function(
    "llava_image_embed_make_with_filename",
    [clip_ctx_p_ctypes, c_int, c_char_p],
    POINTER(llava_image_embed),
)
def llava_image_embed_make_with_filename(
    ctx_clip: clip_ctx_p, n_threads: Union[c_int, int], image_path: bytes, /
) -> "_Pointer[llava_image_embed]":
    ...


# LLAVA_API void llava_image_embed_free(struct llava_image_embed * embed);
# /** free an embedding made with llava_image_embed_make_* */
@ctypes_function("llava_image_embed_free", [POINTER(llava_image_embed)], None)
def llava_image_embed_free(embed: "_Pointer[llava_image_embed]", /):
    ...


# /** write the image represented by embed into the llama context with batch size n_batch, starting at context pos n_past. on completion, n_past points to the next position in the context after the image embed. */
# LLAVA_API bool llava_eval_image_embed(struct llama_context * ctx_llama, const struct llava_image_embed * embed, int n_batch, int * n_past);
@ctypes_function(
    "llava_eval_image_embed",
    [
        llama_cpp.llama_context_p_ctypes,
        POINTER(llava_image_embed),
        c_int,
        POINTER(c_int),
    ],
    c_bool,
)
def llava_eval_image_embed(
    ctx_llama: llama_cpp.llama_context_p,
    embed: "_Pointer[llava_image_embed]",
    n_batch: Union[c_int, int],
    n_past: "_Pointer[c_int]",
    /,
) -> bool:
    ...


################################################
# clip.h
################################################


# /** load mmproj model */
# CLIP_API struct clip_ctx * clip_model_load    (const char * fname, int verbosity);
@ctypes_function("clip_model_load", [c_char_p, c_int], clip_ctx_p_ctypes)
def clip_model_load(
    fname: bytes, verbosity: Union[c_int, int], /
) -> Optional[clip_ctx_p]:
    ...


# /** free mmproj model */
# CLIP_API void clip_free(struct clip_ctx * ctx);
@ctypes_function("clip_free", [clip_ctx_p_ctypes], None)
def clip_free(ctx: clip_ctx_p, /):
    ...


# CLIP_API struct clip_image_u8  * clip_image_u8_init ();
@ctypes_function("clip_image_u8_init", [], c_void_p)
def clip_image_u8_init() -> Optional[c_void_p]:
    ...


# CLIP_API void clip_image_u8_free (struct clip_image_u8  * img);
@ctypes_function("clip_image_u8_free", [c_void_p], None)
def clip_image_u8_free(img: c_void_p, /):
    ...


# CLIP_API struct clip_image_f32_batch * clip_image_f32_batch_init();
@ctypes_function("clip_image_f32_batch_init", [], c_void_p)
def clip_image_f32_batch_init() -> Optional[c_void_p]:
    ...


# CLIP_API void clip_image_f32_batch_free(struct clip_image_f32_batch * batch);
@ctypes_function("clip_image_f32_batch_free", [c_void_p], None)
def clip_image_f32_batch_free(batch: c_void_p, /):
    ...


# /** preprocess img and store the result in res_imgs, pad_to_square may be overridden to false depending on model configuration */
# CLIP_API bool clip_image_preprocess(struct clip_ctx * ctx, const struct clip_image_u8 * img, struct clip_image_f32_batch * res_imgs );
@ctypes_function(
    "clip_image_preprocess",
    [
        clip_ctx_p_ctypes,
        c_void_p,
        c_void_p,
    ],
    c_bool,
)
def clip_image_preprocess(
    ctx: clip_ctx_p,
    img: c_void_p,
    res_imgs: c_void_p,
    /,
) -> bool:
    ...


# CLIP_API bool clip_image_batch_encode(struct clip_ctx * ctx, int n_threads, const struct clip_image_f32_batch * imgs, float * vec);
@ctypes_function(
    "clip_image_batch_encode",
    [
        clip_ctx_p_ctypes,
        c_int,
        c_void_p,
        POINTER(c_float),
    ],
    c_bool,
)
def clip_image_batch_encode(
    ctx: clip_ctx_p,
    n_threads: c_int,
    imgs: c_void_p,
    vec: c_void_p,
    /,
) -> bool:
    ...


# /** interpret bytes as an image file with length bytes_length, and use the result to populate img */
# CLIP_API bool clip_image_load_from_bytes(const unsigned char * bytes, size_t bytes_length, struct clip_image_u8 * img);
@ctypes_function(
    "clip_image_load_from_bytes",
    [
        c_void_p,
        c_size_t,
        c_void_p,
    ],
    c_bool,
)
def clip_image_load_from_bytes(
    bytes: c_void_p,
    bytes_length: c_size_t,
    img: c_void_p,
    /,
) -> bool:
    ...
