package com.example.productcatalog

import android.content.Context
import org.json.JSONArray
import java.text.NumberFormat
import java.util.Locale

object ProductRepository {
    fun load(context: Context): ArrayList<Product> {
        val json = context.assets.open("database.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
        val records = JSONArray(json)
        val products = ArrayList<Product>(records.length())
        for (index in 0 until records.length()) {
            val item = records.getJSONObject(index)
            products.add(
                Product(
                    code = item.getString("code"),
                    name = item.getString("name"),
                    price = item.getLong("price"),
                    category = item.getString("category"),
                    image = item.getString("image"),
                    description = item.getString("description")
                )
            )
        }
        return products
    }

    fun formatPrice(price: Long): String =
        NumberFormat.getCurrencyInstance(Locale("vi", "VN")).format(price)
}
