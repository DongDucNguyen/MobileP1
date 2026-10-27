package com.example.productcatalog

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.widget.ImageView
import android.util.LruCache

object ProductImages {
    private const val ASSET_PREFIX = "file:///android_asset/"
    private val cache = object : LruCache<String, Bitmap>(8 * 1024 * 1024) {
        override fun sizeOf(key: String, value: Bitmap): Int = value.byteCount
    }

    fun show(context: Context, imageUrl: String, view: ImageView) {
        val image = cache.get(imageUrl) ?: load(context, imageUrl)?.also { cache.put(imageUrl, it) }
        view.setImageBitmap(image)
    }

    private fun load(context: Context, imageUrl: String): Bitmap? {
        if (!imageUrl.startsWith(ASSET_PREFIX)) return null
        val assetPath = imageUrl.removePrefix(ASSET_PREFIX)
        return try {
            context.assets.open(assetPath).use(BitmapFactory::decodeStream)
        } catch (_: Exception) {
            null
        }
    }
}
