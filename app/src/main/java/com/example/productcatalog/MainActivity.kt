package com.example.productcatalog

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.view.inputmethod.InputMethodManager
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import java.text.Normalizer
import java.util.Locale

class MainActivity : Activity() {
    private val allProducts = ArrayList<Product>()
    private val visibleProducts = ArrayList<Product>()
    private lateinit var productAdapter: ProductAdapter
    private lateinit var categorySpinner: Spinner
    private lateinit var searchInput: EditText
    private lateinit var resultCount: TextView
    private var searchActive = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        categorySpinner = findViewById(R.id.categorySpinner)
        searchInput = findViewById(R.id.searchInput)
        resultCount = findViewById(R.id.resultCount)
        val productList = findViewById<ListView>(R.id.productList)

        try {
            allProducts.addAll(ProductRepository.load(this))
        } catch (_: Exception) {
            Toast.makeText(this, "Không thể đọc database.json", Toast.LENGTH_LONG).show()
        }

        productAdapter = ProductAdapter(this, visibleProducts)
        productList.adapter = productAdapter // setAdapter cho ArrayAdapter<Product>
        productList.emptyView = findViewById(R.id.emptyMessage)
        productList.onItemClickListener = AdapterView.OnItemClickListener { _, _, position, _ ->
            val product = productAdapter.getItem(position) ?: return@OnItemClickListener
            startActivity(Intent(this, ProductDetailActivity::class.java).putExtra("product_code", product.code))
        }

        val categories = arrayListOf("Tất cả")
        categories.addAll(allProducts.map { it.category }.distinct())
        categorySpinner.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            categories
        )
        categorySpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                if (searchActive && position == 0) return
                searchActive = false
                searchInput.text.clear()
                val category = categories[position]
                showProducts(if (position == 0) allProducts else allProducts.filter { it.category == category })
            }

            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }

        findViewById<Button>(R.id.searchButton).setOnClickListener { performSearch() }
        searchInput.setOnEditorActionListener { _, _, event ->
            if (event == null || event.keyCode == KeyEvent.KEYCODE_ENTER) {
                performSearch()
                true
            } else false
        }
        showProducts(allProducts)
    }

    private fun performSearch() {
        val query = normalize(searchInput.text.toString().trim())
        searchActive = query.isNotEmpty()
        if (categorySpinner.selectedItemPosition != 0) categorySpinner.setSelection(0)
        val matches = if (query.isEmpty()) allProducts else allProducts.filter {
            normalize(it.name).contains(query) || normalize(it.code).contains(query)
        }
        showProducts(matches)
        (getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager)
            .hideSoftInputFromWindow(searchInput.windowToken, 0)
        searchInput.clearFocus()
    }

    private fun showProducts(products: List<Product>) {
        visibleProducts.clear()
        visibleProducts.addAll(products)
        productAdapter.notifyDataSetChanged()
        resultCount.text = "${visibleProducts.size} sản phẩm"
    }

    private fun normalize(value: String): String = Normalizer.normalize(value, Normalizer.Form.NFD)
        .replace(Regex("\\p{M}+"), "")
        .replace('đ', 'd')
        .replace('Đ', 'D')
        .lowercase(Locale.ROOT)
}
