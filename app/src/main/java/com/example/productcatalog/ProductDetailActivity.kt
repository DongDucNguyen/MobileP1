package com.example.productcatalog

import android.app.Activity
import android.os.Bundle
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast

class ProductDetailActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_product_detail)

        val code = intent.getStringExtra("product_code")
        val product = try {
            ProductRepository.load(this).firstOrNull { it.code == code }
        } catch (_: Exception) {
            null
        }
        if (product == null) {
            Toast.makeText(this, "Không tìm thấy sản phẩm", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        findViewById<TextView>(R.id.backButton).setOnClickListener { finish() }
        findViewById<TextView>(R.id.detailName).text = product.name
        ProductImages.show(this, product.image, findViewById<ImageView>(R.id.detailImage))
        findViewById<TextView>(R.id.detailDescription).text = product.description
        findViewById<TextView>(R.id.detailPrice).text = ProductRepository.formatPrice(product.price)
        findViewById<TextView>(R.id.detailCategory).text = "Danh mục: ${product.category}"
        findViewById<TextView>(R.id.detailCode).text = "Mã sản phẩm: ${product.code}"
    }
}
