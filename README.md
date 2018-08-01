# Prerequisites

* Python 3
* Flask (for Python 3)

# Running the website

1. Apply the following patch, since Flask will run on a different port:
```diff
diff --git a/index.html b/index.html
index 57d2c5a..5c8be9b 100644
--- a/index.html
+++ b/index.html
@@ -95,7 +95,7 @@
                                         <input type="text" class="form-control" name="lastName" placeholder="Last name" required>
                                     </div>
                                     <div class="col-auto">
-                                        <button type="submit" formaction="/database/getInfo" class="btn btn-primary mb-2">Lookup Guest</button>
+                                        <button type="submit" formaction="http://localhost:5000/getInfo" class="btn btn-primary mb-2">Lookup Guest</button>
                                     </div>
                                 </div>
                             </form>
@@ -126,7 +126,7 @@
                                         <label class="form-check-label" for="vegetarianNo">No</label>
                                     </div>
                                 </fieldset>
-                                <button type="submit" formaction="/database/updateInfo" class="btn btn-primary mb-2">Update Info</button>
+                                <button type="submit" formaction="http://localhost:5000/updateInfo" class="btn btn-primary mb-2">Update Info</button>
                             </form>
                         </div>
                     </div>
```
2. From the python directory, run `./weddingWebsite.py`.
3. At the same time, from the current directory, run `python3 -m http.server 8080`.
4. Navigate to `http://localhost:8080/` and use the website.
